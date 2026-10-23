from pydantic import BaseModel
from typing import Optional, Dict, Any

class SecretRequest(BaseModel):
    name: str
    type: str = "arbitrary"
    version: Optional[str] = None

class SecretResponse(BaseModel):
    value: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

def normalize_secret_response(raw_response: Dict[str, Any]) -> SecretResponse:
    return SecretResponse(
        value=raw_response.get("value"),
        version=raw_response.get("version"),
        metadata=raw_response.get("metadata")
    )