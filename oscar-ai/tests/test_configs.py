import pytest
from pydantic import ValidationError

from src.configs import ModelConfig, OpenAIProviderConfig, Requirements


def test_model_config_defaults_temperature_and_max_tokens():
    config = ModelConfig(model="gemini")

    assert config.temperature == 0.7
    assert config.max_tokens == 1024


def test_model_config_rejects_empty_model():
    with pytest.raises(ValidationError):
        ModelConfig(model="")


def test_model_config_rejects_invalid_temperature():
    with pytest.raises(ValidationError):
        ModelConfig(model="gemini", temperature=1.1)

    with pytest.raises(ValidationError):
        ModelConfig(model="gemini", temperature=-0.1)


def test_model_config_rejects_invalid_max_tokens():
    with pytest.raises(ValidationError):
        ModelConfig(model="gemini", max_tokens=0)

    with pytest.raises(ValidationError):
        ModelConfig(model="gemini", max_tokens=-100)


def test_openai_provider_config_requires_endpoint():
    with pytest.raises(ValidationError):
        OpenAIProviderConfig()


def test_openai_provider_config_accepts_none_api_key():
    config = OpenAIProviderConfig(endpoint="https://api.example.com")

    assert config.api_key is None
    assert config.endpoint == "https://api.example.com"


def test_requirements_rejects_empty_id():
    with pytest.raises(ValidationError):
        Requirements(id="")
