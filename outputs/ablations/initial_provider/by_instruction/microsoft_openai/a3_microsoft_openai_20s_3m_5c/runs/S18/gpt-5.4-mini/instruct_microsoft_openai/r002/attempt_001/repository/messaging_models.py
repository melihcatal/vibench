import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PublishRequest:
    event_type: str
    payload: Dict[str, Any]
    message_id: Optional[str] = None


@dataclass
class PublishResponse:
    message_id: str
    accepted: bool


def to_json_text(data: Dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


def normalize_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for record in records:
        item = dict(record)
        if "message_id" not in item and "id" in item:
            item["message_id"] = item["id"]
        normalized.append(item)
    return normalized
