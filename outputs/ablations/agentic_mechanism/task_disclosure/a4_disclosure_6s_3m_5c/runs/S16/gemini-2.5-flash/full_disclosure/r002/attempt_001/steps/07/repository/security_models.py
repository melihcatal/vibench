
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class SecretRequest:
    name: str
    version: Optional[str] = None
    project_id: Optional[str] = None

@dataclass
class SecretResponse:
    name: str
    version: str
    data: Any
    project_id: Optional[str] = None
    create_time: Optional[str] = None
    update_time: Optional[str] = None

def normalize_secret_data(data: Any) -> Dict[str, Any]:
    """
    Normalizes the secret data into a dictionary format.
    This is a placeholder for actual normalization logic.
    """
    if isinstance(data, dict):
        return data
    elif isinstance(data, str):
        # Attempt to parse as JSON, otherwise return as a string in a dict
        try:
            import json
            return json.loads(data)
        except json.JSONDecodeError:
            return {"value": data}
    else:
        return {"value": str(data)}
