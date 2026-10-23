from typing import Dict, Any, Optional
from pydantic import BaseModel

class ModelRequest(BaseModel):
    prompt: str
    model_identifier: str
    temperature: float = 0.7
    max_tokens: int = 1000

class ModelResponse(BaseModel):
    output: str
    metadata: Dict[str, Any]