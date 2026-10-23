import json
from dataclasses import dataclass, asdict


@dataclass
class MessagePayload:
    message_id: str
    content: str
    attributes: dict


@dataclass
class PublishResult:
    message_id: str
    accepted: bool


@dataclass
class ConsumeResult:
    message_id: str
    body: str
    delivery_count: int


def payload_to_json(payload: MessagePayload) -> str:
    return json.dumps(asdict(payload), ensure_ascii=False)


def json_to_payload(value: str) -> MessagePayload:
    data = json.loads(value)
    return MessagePayload(
        message_id=data["message_id"],
        content=data["content"],
        attributes=data.get("attributes", {}),
    )
