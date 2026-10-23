from pydantic import BaseModel
from typing import List, Dict, Any


class ModelRequest(BaseModel):
    prompt: str
    context: str = ""
    model: str = "gpt-4o"
    max_tokens: int = 150
    temperature: float = 0.7


class ModelResponse(BaseModel):
    text: str
    finish_reason: str
    model: str
    usage: Dict[str, int]


class JSONModelResponse(BaseModel):
    json_object: Dict[str, Any]
    model: str
    usage: Dict[str, int]
