from dataclasses import dataclass
from typing import Optional, Dict, Any
import json

@dataclass
class SecretConfig:
    name: str
    version: Optional[str] = None
    project_id: Optional[str] = None
    vault_url: Optional[str] = None

@dataclass
class SecretResponse:
    value: str
    version: str
    created_time: Optional[str] = None

def parse_json_secret(secret_str: str) -> Dict[str, Any]:
    """Parse JSON formatted secret."""
    return json.loads(secret_str)