from pydantic import BaseModel
from typing import Optional, Dict, Any

class SecretResponse(BaseModel):
    value: str
    metadata: Optional[Dict[str, Any]] = None
    labels: Optional[Dict[str, str]] = None
    version: Optional[str] = None