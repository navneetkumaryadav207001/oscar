from Chat import Chat
from pydantic import BaseModel, Field

class ModelConfig(BaseModel):
    # NOTE: Pending Cross Entity Validation
    # KnownModels Defaulting Functionality Missing
    model: str = Field(min_length=1)
    api_key: str = Field(min_length=1)
    endpoint: str | None = None
    temperature: float | int = Field(default=0.7, ge=0, le=1)
    max_tokens: int = Field(default=1024, gt=0)

class Model:
    def __init__(self, config: ModelConfig):
        self.config = config

    def _call_llm(prompt: str):
        pass
        # data = requests.post(self.endpoint, body = {
        #     api_key = self.api_key,
        #     temperature = self.temperature,
        #     max_tokens = self.max_tokens,
        #     message = prompt
        # })

    def generate(prompt: Chat):
        pass
        # generation = self._call_llm(prompt.to_str())
        # return generation

    def stream(prompt: Chat):
        pass
        ## Need to understand streaming

    def tool_call(prompt:Chat):
        pass


