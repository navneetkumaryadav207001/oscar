
from model import Model
from chat import Chat

class Router:
    def __init__(self):
        self.models : list[Model] = []

    def generate(self,prompt:Chat, requirements: Requirements):
        model = self.resolve(requirements)
        model.generate(prompt)

    def stream(self,prompt:Chat, requirements: Requirements):
        model = self.resolve(requirements)
        model.generate(prompt)

    def resolve(requirements:Requirements):
        """Logic For resolving Requirements"""