# Placeholder for request/response normalization models
from typing import TypedDict, Any

class SecretRequest(TypedDict):
    name: str
    version_stage: str | None = None

class SecretResponse(TypedDict):
    value: str

class JsonSecretResponse(SecretResponse):
    parsed: Any
