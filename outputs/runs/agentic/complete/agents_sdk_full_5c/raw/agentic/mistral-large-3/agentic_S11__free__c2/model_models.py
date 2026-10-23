from pydantic import BaseModel
from typing import Optional

class ModelRequest(BaseModel):
    message: str
    temperature: float = 0.7
    max_tokens: int = 1000
    model: str = "command-r-plus"

class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class BilledUnits(BaseModel):
    input_tokens: int
    output_tokens: int

class ModelResponseMetadata(BaseModel):
    billed_units: Optional[BilledUnits] = None
    tokens: Optional[TokenUsage] = None
    model: Optional[str] = None

class ModelResponse(BaseModel):
    text: str
    model: Optional[str] = None
    token_count: Optional[int] = None
    meta: Optional[ModelResponseMetadata] = None