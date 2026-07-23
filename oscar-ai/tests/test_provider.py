import pytest
from collections.abc import Iterator

from src.chat import Chat
from src.configs import ModelConfig
from src.provider import Provider


class DummyProvider(Provider):
    def generate(self, model_config: ModelConfig, prompt: Chat) -> str:
        return "generated"

    def stream(self, model_config: ModelConfig, prompt: Chat) -> Iterator[str]:
        yield "chunk-1"
        yield "chunk-2"


def test_provider_tool_call_raises_not_implemented():
    provider = DummyProvider()
    config = ModelConfig(model="gemini", temperature=0.7, max_tokens=1)

    with pytest.raises(NotImplementedError, match="does not support tool calling"):
        provider.tool_call(config)


def test_provider_generate_and_stream_work_as_expected():
    provider = DummyProvider()
    chat = Chat()
    chat.add_user("hi")
    config = ModelConfig(model="gemini", temperature=0.7, max_tokens=1)

    assert provider.generate(config, chat) == "generated"
    assert list(provider.stream(config, chat)) == ["chunk-1", "chunk-2"]
