from dataclasses import dataclass
from typing import Optional


@dataclass
class SecretRequest:
    project_id: str
    secret_id: str
    version_id: str = "latest"


@dataclass
class SecretResponse:
    name: str
    payload: Optional[str] = None
    version: Optional[str] = None
