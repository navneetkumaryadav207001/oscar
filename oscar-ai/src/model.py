from collections.abc import Iterator
from chat import Chat
from provider import Provider
from configs import ModelConfig

class Model:
    def __init__(self, config: ModelConfig, provider: Provider):
        self.config = config
        self.provider = provider

    def generate(self, prompt: Chat) -> str:
        return self.provider.generate(prompt = prompt, model_config= self.config)

    def stream(self, prompt: Chat) -> Iterator[str]:
        return self.provider.stream(prompt = prompt, model_config= self.config)