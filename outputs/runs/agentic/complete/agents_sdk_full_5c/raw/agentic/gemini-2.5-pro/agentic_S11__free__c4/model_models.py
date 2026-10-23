from typing import Any, Dict, Optional
from pydantic import BaseModel

class CompletionRequest(BaseModel):
    prompt: str
    model: str = "command-r"

class CompletionResponse(BaseModel):
    text: str
    metadata: Dict[str, Any]
    model: Optional[str] = None
