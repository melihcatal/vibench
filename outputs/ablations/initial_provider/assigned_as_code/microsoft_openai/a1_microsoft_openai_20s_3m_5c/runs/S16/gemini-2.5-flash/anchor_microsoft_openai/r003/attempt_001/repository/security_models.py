from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class SecretPayload:
    project_id: str
    secret_id: str
    version_id: str = "latest"

@dataclass
class SecretResponse:
    secret_id: str
    version_id: str
    data: str | Dict[str, Any]

def normalize_json_secret(secret_data: str) -> Dict[str, Any]:
    """
    Normalizes a JSON string secret into a dictionary.
    """
    import json
    return json.loads(secret_data)

def normalize_text_secret(secret_data: str) -> str:
    """
    Normalizes a text secret.
    """
    return secret_data
