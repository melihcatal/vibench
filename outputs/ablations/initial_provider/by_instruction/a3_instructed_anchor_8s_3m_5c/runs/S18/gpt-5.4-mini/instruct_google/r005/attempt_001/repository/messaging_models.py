import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"message": payload}
    return {"value": payload}


@dataclass
class PublishRequest:
    data: Dict[str, Any]
    attributes: Dict[str, str]


@dataclass
class PublishResponse:
    message_ids: List[str]


@dataclass
class ConsumeResponse:
    message_id: Optional[str]
    payload: Dict[str, Any]
    attributes: Dict[str, str]


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj) if hasattr(obj, "__dataclass_fields__") else dict(obj)
