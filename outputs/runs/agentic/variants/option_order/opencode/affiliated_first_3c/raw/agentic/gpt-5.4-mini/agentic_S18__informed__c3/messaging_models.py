import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload.strip()
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def ensure_json_dict(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str) and payload.strip():
        return json.loads(payload)
    return {}


@dataclass
class PublishResult:
    message_id: str
    success: bool
    provider: str
    attributes: Dict[str, Any]


@dataclass
class ConsumeResult:
    message_id: str
    body: str
    attributes: Dict[str, Any]
    provider: str


@dataclass
class BatchPublishItem:
    message_id: str
    body: Any
    attributes: Optional[Dict[str, Any]] = None


def dataclass_to_dict(value: Any) -> Dict[str, Any]:
    return asdict(value)


def parse_batch_items(items: List[Dict[str, Any]]) -> List[BatchPublishItem]:
    return [
        BatchPublishItem(
            message_id=str(item.get("message_id", "")),
            body=item.get("body"),
            attributes=item.get("attributes"),
        )
        for item in items
    ]
