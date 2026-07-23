from src.chat import Chat
from src.model import Model, ModelConfig
from pydantic import ValidationError
import pytest


@pytest.fixture
def make_model_config():
    return ModelConfig(model="gemini", temperature=0.7, max_tokens=1024)


class DummyProvider:
    def __init__(self):
        self.generated = False
        self.streamed = False

    def generate(self, model_config: ModelConfig, prompt: Chat) -> str:
        self.generated = True
        return f"generated:{model_config.model}:{prompt.to_dict()}"

    def stream(self, model_config: ModelConfig, prompt: Chat):
        self.streamed = True
        yield f"streamed:{model_config.model}"


class TestModelConfig:
    def test_default_values_are_applied(self, make_model_config):
        assert make_model_config.temperature == 0.7
        assert make_model_config.max_tokens == 1024

    def test_empty_model_name_rejected(self):
        with pytest.raises(ValidationError):
            ModelConfig(model="")

    def test_invalid_temperature_rejected(self):
        with pytest.raises(ValidationError):
            ModelConfig(model="gemini", temperature=1.1)

        with pytest.raises(ValidationError):
            ModelConfig(model="gemini", temperature=-0.1)

    def test_invalid_max_tokens_rejected(self):
        with pytest.raises(ValidationError):
            ModelConfig(model="gemini", max_tokens=0)

        with pytest.raises(ValidationError):
            ModelConfig(model="gemini", max_tokens=-5)


class TestModel:
    def test_generate_delegates_to_provider(self, make_model_config):
        provider = DummyProvider()
        model = Model(config=make_model_config, provider=provider)
        prompt = Chat()
        prompt.add_user("hello")

        result = model.generate(prompt)

        assert provider.generated is True
        assert result == f"generated:gemini:{prompt.to_dict()}"

    def test_stream_returns_provider_iterator(self, make_model_config):
        provider = DummyProvider()
        model = Model(config=make_model_config, provider=provider)
        prompt = Chat()
        prompt.add_user("hello")

        result = list(model.stream(prompt))

        assert provider.streamed is True
        assert result == ["streamed:gemini"]

