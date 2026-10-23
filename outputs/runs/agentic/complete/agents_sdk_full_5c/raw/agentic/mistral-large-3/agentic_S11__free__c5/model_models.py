from typing import NamedTuple, Optional, Any
from dataclasses import dataclass

@dataclass
class ModelRequest:
    message: str
    temperature: float
    max_tokens: int
    model: str

@dataclass
class ModelResponse:
    text: str
    model: str
    response_id: Optional[str]
    meta: Optional[Any]