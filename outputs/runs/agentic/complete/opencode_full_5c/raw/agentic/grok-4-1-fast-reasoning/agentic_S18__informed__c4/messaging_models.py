from dataclasses import dataclass, field
from typing import Dict, Any
import json
import base64


@dataclass
class PubSubMessage:
    id: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    attributes: Dict[str, str] = field(default_factory=dict)


def encode_message_data(data: Dict[str, Any]) -> bytes:
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


def decode_message_data(data: bytes) -> Dict[str, Any]:
    return json.loads(base64.b64decode(data).decode("utf-8"))
