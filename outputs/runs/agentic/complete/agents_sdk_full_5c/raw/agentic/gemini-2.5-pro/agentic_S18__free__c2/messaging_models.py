from dataclasses import dataclass, asdict
import json

@dataclass
class EventPayload:
    event_id: str
    user_id: str
    data: dict

    def to_json(self) -> str:
        return json.dumps(asdict(self))

@dataclass
class ProcessedMessage:
    message_id: str
    original_payload: str
    is_safe: bool
    translation: str
    summary: str
    status: str
