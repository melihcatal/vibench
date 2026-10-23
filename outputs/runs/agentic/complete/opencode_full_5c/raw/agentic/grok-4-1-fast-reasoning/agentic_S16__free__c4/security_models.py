from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class SecretResponse:
    value: str
    version_id: Optional[str] = None


@dataclass
class JsonSecretResponse:
    data: Dict[str, Any]
    version_id: Optional[str] = None
