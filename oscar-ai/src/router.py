
from .model import Model
from .chat import Chat
from .configs import Requirements

class Registry:
    def __init__(self):
        self.models: dict[str, Model] = {}

    def register_model(self, id: str, model: Model):
        if id in self.models:
            raise ValueError(f"Model '{id}' is already registered")

        self.models[id] = model

    def get_model(self, id: str) -> Model:
        try:
            return self.models[id]
        except KeyError:
            raise KeyError(f"Model '{id}' is not registered")

    def list_models(self) -> list[str]:
        return list(self.models.keys())

class Router:
    def __init__(self, registry: Registry):
        self.registry = registry

    def generate(self, prompt: Chat, requirements: Requirements):
        model = self.resolve(requirements)
        return model.generate(prompt)

    def stream(self, prompt: Chat, requirements: Requirements):
        model = self.resolve(requirements)
        return model.stream(prompt)

    def resolve(self, requirements: Requirements) -> Model:
        return self.registry.get_model(requirements.id)
