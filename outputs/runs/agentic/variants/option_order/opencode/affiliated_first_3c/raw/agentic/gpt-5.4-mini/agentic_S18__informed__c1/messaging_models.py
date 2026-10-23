import json
from dataclasses import dataclass, asdict


@dataclass
class PublishRequest:
    message_id: str
    payload: dict
    attributes: dict


@dataclass
class ConsumeResult:
    message_id: str
    payload: dict
    attributes: dict
    ack_id: str | None = None


@dataclass
class BatchPublishItem:
    message_id: str
    payload: dict
    attributes: dict


def to_json_bytes(payload):
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def normalize_record(message_id, payload, attributes):
    return asdict(
        PublishRequest(message_id=message_id, payload=payload, attributes=attributes)
    )
