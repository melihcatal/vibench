import json
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class SecretPayload:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: str = "AWSCURRENT"
    key_field: Optional[str] = None


@dataclass
class ParsedSecret:
    data: Dict[str, Any]

    @classmethod
    def from_secret_string(cls, secret_string: str):
        return cls(data=json.loads(secret_string))
