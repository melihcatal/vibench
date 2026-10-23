from typing import Any, Dict, Optional
from pydantic import BaseModel


class ModelResponse(BaseModel):
    text: str
    raw_response: Optional[Any] = None


class ModelResponseWithMetadata(ModelResponse):
    metadata: Dict[str, Any]
