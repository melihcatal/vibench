import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {str(k): v for k, v in payload.items() if v is not None}


def to_json_bytes(payload: Dict[str, Any]) -> bytes:
    return json.dumps(normalize_payload(payload), separators=(",", ":")).encode("utf-8")


@dataclass
class MessageRequest:
    body: Dict[str, Any]
    message_id: Optional[str] = None
    content_type: str = "application/json"


@dataclass
class MessageResponse:
    message_id: str
    status: str
    details: Dict[str, Any]


@dataclass
class BatchMessageRequest:
    messages: List[MessageRequest]


def response_dict(response: MessageResponse) -> Dict[str, Any]:
    return asdict(response)
