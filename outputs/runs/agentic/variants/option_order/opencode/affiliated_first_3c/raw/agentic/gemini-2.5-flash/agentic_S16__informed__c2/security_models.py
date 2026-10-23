from dataclasses import dataclass
import json
from typing import Any, Dict


@dataclass
class SecretPayload:
    data: str
    data_crc32c: int = None


@dataclass
class SecretVersion:
    name: str
    state: str
    create_time: str
    destroy_time: str = None
    payload: SecretPayload = None


@dataclass
class ParsedJsonSecret:
    payload: Dict[str, Any]

    @classmethod
    def from_string(cls, json_string: str) -> "ParsedJsonSecret":
        return cls(payload=json.loads(json_string))
