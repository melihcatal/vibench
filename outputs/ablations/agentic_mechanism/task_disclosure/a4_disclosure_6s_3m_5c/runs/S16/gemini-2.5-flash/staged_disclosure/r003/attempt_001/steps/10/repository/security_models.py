
import os
from typing import Dict, Any

class SecretRequest:
    def __init__(self, name: str, version: str = "latest"):
        self.name = name
        self.version = version

class SecretResponse:
    def __init__(self, name: str, value: str, version: str):
        self.name = name
        self.value = value
        self.version = version

def normalize_secret_name(name: str) -> str:
    """Normalizes a secret name to a consistent format."""
    return name.strip().lower().replace(" ", "-")

def get_secret_from_env(name: str) -> SecretResponse | None:
    """Retrieves a secret from environment variables."""
    normalized_name = normalize_secret_name(name).upper().replace("-", "_")
    secret_value = os.getenv(normalized_name)
    if secret_value is not None:
        return SecretResponse(name=name, value=secret_value, version="env")
    return None
