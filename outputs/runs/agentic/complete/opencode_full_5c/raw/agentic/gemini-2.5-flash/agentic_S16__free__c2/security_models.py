import json
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class SecretPayload:
    name: str
    data: str
    version: str


@dataclass
class SecretMetadata:
    name: str
    labels: Dict[str, str] = field(default_factory=dict)
    create_time: Optional[str] = None
    rotation_period: Optional[str] = None
