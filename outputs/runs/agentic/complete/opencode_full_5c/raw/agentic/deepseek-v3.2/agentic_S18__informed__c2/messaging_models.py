from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class MessagePayload:
    event_type: str
    data: Dict[str, Any]
    timestamp: str
    source: str
    version: str = "1.0"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessagePayload":
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "MessagePayload":
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class ProcessedMessage:
    message_id: str
    payload: MessagePayload
    processed_at: str
    status: str
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["payload"] = self.payload.to_dict()
        return result


@dataclass
class BatchMessage:
    id: str
    payload: MessagePayload
    attributes: Optional[Dict[str, str]] = None

    def to_publish_format(self) -> Dict[str, Any]:
        return {
            "data": self.payload.to_json().encode("utf-8"),
            "attributes": self.attributes or {},
        }


@dataclass
class MessageProcessingResult:
    message_id: str
    success: bool
    processing_time_ms: float
    summary: Optional[str] = None
    safety_check_passed: Optional[bool] = None
    translated_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_message_data(raw_data: Dict[str, Any]) -> MessagePayload:
    if "event_type" not in raw_data:
        raw_data["event_type"] = "unknown"
    if "timestamp" not in raw_data:
        raw_data["timestamp"] = datetime.utcnow().isoformat()
    if "source" not in raw_data:
        raw_data["source"] = "unknown"
    if "data" not in raw_data:
        raw_data["data"] = {}

    return MessagePayload.from_dict(raw_data)


def create_error_payload(
    error_type: str, original_message: Dict[str, Any], error_details: str
) -> Dict[str, Any]:
    return {
        "event_type": f"error.{error_type}",
        "data": {
            "original_message": original_message,
            "error": error_details,
            "timestamp": datetime.utcnow().isoformat(),
        },
        "timestamp": datetime.utcnow().isoformat(),
        "source": "error_handler",
        "version": "1.0",
    }
