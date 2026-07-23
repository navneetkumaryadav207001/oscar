from pydantic import BaseModel, Field
from typing import Optional

class Message(BaseModel): 
    role: str 
    content: str

class ModelConfig(BaseModel):
    model: str = Field(min_length=1)
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: int = Field(default=1024, gt=0)
    
class OpenAIProviderConfig(BaseModel):
    api_key: Optional[str] = None
    endpoint: str

class Requirements(BaseModel):
    id : str = Field(min_length=1)