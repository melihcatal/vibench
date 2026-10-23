from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class SecretRequest:
    name: str
    version: Optional[str] = None
    project: Optional[str] = None
    config: Optional[str] = None

@dataclass
class SecretResponse:
    value: str
    version: str
    metadata: Optional[Dict[str, Any]] = None