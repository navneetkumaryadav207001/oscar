from collections.abc import Iterator
import json
import requests
from chat import Chat
from provider import Provider
from configs import OpenAIProviderConfig, ModelConfig


class OpenAICompatibleProvider(Provider):
    def __init__(self, endpoint: str, api_key: str | None = None):
        self.config = OpenAIProviderConfig(endpoint=endpoint, api_key=api_key)
        
    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def generate(self, model_config: ModelConfig, prompt: Chat) -> str:
        response = requests.post(
            self.config.endpoint,
            headers=self._headers(),
            json={
                "model": model_config.model,
                "messages": prompt.to_dict(),
                "temperature": model_config.temperature,
                "max_tokens": model_config.max_tokens,
            },
        )

        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def stream(self, model_config: ModelConfig, prompt: Chat) -> Iterator[str]:
        with requests.post(
            self.config.endpoint,
            headers=self._headers(),
            json={
                "model": model_config.model,
                "messages": prompt.to_dict(),
                "temperature": model_config.temperature,
                "max_tokens": model_config.max_tokens,
                "stream": True,
            },
            stream=True,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue

                if isinstance(line, bytes):
                    line = line.decode("utf-8", errors="replace")

                stripped = line.strip()
                if stripped == "[DONE]":
                    break

                if stripped.startswith("data:"):
                    stripped = stripped[len("data:") :].strip()
                else:
                    continue

                if stripped == "[DONE]":
                    break

                try:
                    payload = json.loads(stripped)
                except json.JSONDecodeError:
                    continue

                choices = payload.get("choices") or []
                if not choices:
                    continue

                delta = choices[0].get("delta") or {}
                content = delta.get("content")
                if content is not None:
                    yield content
