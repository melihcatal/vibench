from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class PlatformRequest(BaseModel):
    """A standardized request model for platform invocations."""
    prompt: str
    model_id: str = "command-r"
    max_tokens: int = 150
    temperature: float = 0.7

class PlatformResponse(BaseModel):
    """A standardized response model from a platform invocation."""
    text: str
    model_id: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
