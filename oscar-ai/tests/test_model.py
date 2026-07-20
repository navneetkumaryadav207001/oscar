from model import Model, ModelConfig
from pydantic import ValidationError
import pytest

@pytest.fixture
def make_config():
    def _make_config(**overrides):
        defaults = {
            "model": "gemini",
            "api_key": "test",
            "endpoint": None,
            "temperature": 0.7,
            "max_tokens": 1024,
        }
        defaults.update(overrides)
        return ModelConfig(**defaults)

    return _make_config

class TestModelConfig:
    class TestDefault:
        def test_constructor_uses_default_temperature_when_not_provided(self,make_config):
            assert make_config().temperature == 0.7
        def test_constructor_uses_default_maxtokens_when_not_provided(self,make_config):
            assert make_config().max_tokens == 1024
        def test_constructor_sets_endpoint_as_None_when_not_provided(self,make_config):
            assert make_config().endpoint == None
            
    class TestInputValidation:
        # Valid Partitions
        def test_model_accepts_str(self,make_config):
            make_config(model="gemini")
        def test_api_key_accepts_str(self,make_config):
            make_config(api_key="test")
        def test_temperature_accepts_numeric(self,make_config):
            make_config(temperature = 0.7)
            make_config(temperature = 1)
            make_config(temperature = "0.7")
        def test_max_tokens_accepts_int(self,make_config):
            make_config(max_tokens = 1024)
        def test_endpoint_accepts_str(self,make_config):
            make_config(endpoint = "https://gemini.com")

        # Invalid Partitions
        def test_model_rejects_non_str(self,make_config):
            with pytest.raises(ValidationError):
                make_config(model = 123)
        def test_api_key_rejects_non_str(self,make_config):
            with pytest.raises(ValidationError):
                make_config(api_key = 1234)        
        def test_temperature_rejects_non_numeric(self,make_config):
            with pytest.raises(ValidationError):
                make_config(temperature = "test")
            with pytest.raises(ValidationError):
                make_config(temperature = {1,2,3})
        def test_max_tokens_rejects_non_int(self,make_config):
            with pytest.raises(ValidationError):
                make_config(max_tokens = "test")
            with pytest.raises(ValidationError):
                make_config(max_tokens = {1,2,3})
        def test_endpoint_rejects_non_str(self, make_config):
            with pytest.raises(ValidationError):
                make_config(endpoint = 123)

    class TestSemanticValidation:
        pass
    class TestKnownModels:
        pass
    class TestCrossFieldValidation:
        pass
    
    

class TestModel:

    class TestConstructor:
        pass
    class TestGenerate:
        pass
    class TestStream:
        pass
    class TestToolCall:
        pass