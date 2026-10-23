from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json


def normalize_payload(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


@dataclass
class PublishRequest:
    topic_arn: str
    payload: Any
    subject: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class PublishResponse:
    message_id: str
    sequence_number: Optional[str] = None
    provider: str = "aws"


@dataclass
class ConsumeResult:
    message_id: str
    receipt_handle: Optional[str]
    payload: str
    attributes: Dict[str, str] = field(default_factory=dict)
    provider: str = "aws"


@dataclass
class BatchPublishRequest:
    topic_arn: str
    entries: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class BatchPublishResponse:
    successful: List[Dict[str, Any]] = field(default_factory=list)
    failed: List[Dict[str, Any]] = field(default_factory=list)
    provider: str = "aws"
