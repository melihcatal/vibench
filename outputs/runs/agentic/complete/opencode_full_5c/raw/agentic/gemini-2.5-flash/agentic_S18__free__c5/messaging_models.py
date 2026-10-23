import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional


@dataclass
class PubsubMessage:
    data: Dict[str, Any]
    message_id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None

    def to_json(self) -> str:
        return json.dumps(self.data)

    @classmethod
    def from_json(
        cls,
        json_string: str,
        message_id: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
    ):
        return cls(
            data=json.loads(json_string), message_id=message_id, attributes=attributes
        )


@dataclass
class PublishResponse:
    message_ids: list[str]


@dataclass
class ConsumeResponse:
    message: Optional[PubsubMessage]
    ack_id: Optional[str]


@dataclass
class AuditRecord:
    message_id: str
    timestamp: str
    status: str
    payload: Dict[str, Any]
    additional_info: Optional[Dict[str, Any]] = None
