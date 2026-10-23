import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

@dataclass
class EventPayload:
    event_id: str
    type: str
    timestamp: str
    data: Dict[str, Any]
    source: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_string: str):
        data = json.loads(json_string)
        return cls(**data)

@dataclass
class ProcessedMessageRecord:
    message_id: str
    event_type: str
    processed_timestamp: str
    status: str
    summary: Optional[str] = None
    translation_status: Optional[str] = None
    safety_scan_result: Optional[str] = None
    original_payload: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(asdict(self))

if __name__ == "__main__":
    example_payload = EventPayload(
        event_id="test-001",
        type="user_created",
        timestamp="2023-10-27T12:00:00Z",
        data={"user_id": "u-123", "name": "John Doe"},
        source="web-app"
    )
    print("Example EventPayload JSON:", example_payload.to_json())

    deserialized_payload = EventPayload.from_json(example_payload.to_json())
    print("Deserialized EventPayload:", deserialized_payload)

    example_record = ProcessedMessageRecord(
        message_id="msg-abc-789",
        event_type="user_created",
        processed_timestamp="2023-10-27T12:05:00Z",
        status="SUCCESS",
        summary="User creation event processed.",
        original_payload={"user_id": "u-123", "name": "John Doe"}
    )
    print("Example ProcessedMessageRecord Dict:", example_record.to_dict())
