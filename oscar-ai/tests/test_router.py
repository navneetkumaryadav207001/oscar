import pytest
from collections.abc import Iterator

from src.chat import Chat
from src.configs import ModelConfig, Requirements
from src.model import Model
from src.provider import Provider
from src.router import Registry, Router


class DummyProvider(Provider):
    def generate(self, model_config: ModelConfig, prompt: Chat) -> str:
        return f"generated-{model_config.model}"

    def stream(self, model_config: ModelConfig, prompt: Chat) -> Iterator[str]:
        yield f"streamed-{model_config.model}"


def test_registry_registers_and_returns_models():
    registry = Registry()
    model = Model(
        config=ModelConfig(model="gemini", temperature=0.7, max_tokens=1),
        provider=DummyProvider(),
    )

    registry.register_model("gemini-v1", model)

    assert registry.get_model("gemini-v1") is model
    assert registry.list_models() == ["gemini-v1"]


def test_registry_register_duplicate_raises_value_error():
    registry = Registry()
    model = Model(
        config=ModelConfig(model="gemini", temperature=0.7, max_tokens=1),
        provider=DummyProvider(),
    )

    registry.register_model("gemini-v1", model)

    with pytest.raises(ValueError, match="already registered"):
        registry.register_model("gemini-v1", model)


def test_registry_get_model_missing_raises_key_error():
    registry = Registry()

    with pytest.raises(KeyError, match="is not registered"):
        registry.get_model("missing")


def test_router_resolves_requirement_and_generates():
    registry = Registry()
    model = Model(
        config=ModelConfig(model="gemini", temperature=0.7, max_tokens=1),
        provider=DummyProvider(),
    )
    registry.register_model("gemini-v1", model)
    router = Router(registry)
    prompt = Chat()
    prompt.add_user("hello")
    requirements = Requirements(id="gemini-v1")

    assert router.generate(prompt, requirements) == "generated-gemini"
    assert list(router.stream(prompt, requirements)) == ["streamed-gemini"]
