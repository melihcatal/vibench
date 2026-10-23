from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class PublishRequest:
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None


@dataclass
class PublishResponse:
    message_id: str
    success: bool


@dataclass
class ConsumeResponse:
    data: Dict[str, Any]
    message_id: str
    attributes: Optional[Dict[str, str]] = None
    success: bool = True


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: str(v) if v is not None else "" for k, v in payload.items()}
