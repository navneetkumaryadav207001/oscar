
from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any
from configs import ModelConfig

class Provider(ABC):
    @abstractmethod
    def generate(self,model_config:ModelConfig) -> str:
        """Generate a complete response."""

    @abstractmethod
    def stream(self,model_config:ModelConfig) -> Iterator[str]:
        """Generate a response incrementally."""

    def tool_call(self,model_config:ModelConfig) -> Any:
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support tool calling"
        )