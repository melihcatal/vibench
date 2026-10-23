import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
            return parsed if isinstance(parsed, dict) else {"value": parsed}
        except Exception:
            return {"text": payload}
    return {"value": payload}


def to_json_text(payload: Any) -> str:
    return json.dumps(normalize_payload(payload), ensure_ascii=False)


@dataclass
class MessageRecord:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PublishRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]


@dataclass
class PublishResponse:
    provider: str
    message_id: str
    metadata: Dict[str, Any]


def make_batch(records: Iterable[Any]) -> List[MessageRecord]:
    batch: List[MessageRecord] = []
    for index, record in enumerate(records):
        if isinstance(record, MessageRecord):
            batch.append(record)
        elif isinstance(record, dict):
            batch.append(MessageRecord(str(record.get("message_id", index)), normalize_payload(record.get("payload")), {str(k): str(v) for k, v in record.get("attributes", {}).items()}))
        else:
            batch.append(MessageRecord(str(index), normalize_payload(record), {}))
    return batch
