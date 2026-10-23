from typing import TypedDict, Optional, Dict, Any

class SecretRequest(TypedDict):
    secret_id: str
    version: Optional[str]

class SecretResponse(TypedDict):
    name: str
    value: str
    version_id: Optional[str]
    parsed: Optional[Dict[str, Any]]