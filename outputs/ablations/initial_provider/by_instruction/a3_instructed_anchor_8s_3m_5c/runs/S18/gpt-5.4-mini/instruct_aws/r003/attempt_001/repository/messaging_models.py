import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def normalize_payload(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


@dataclass
class MessageRequest:
    message_id: str
    payload: Any
    attributes: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["payload"] = normalize_payload(self.payload)
        return data


@dataclass
class MessageResponse:
    ok: bool
    provider_message_id: str
    detail: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
