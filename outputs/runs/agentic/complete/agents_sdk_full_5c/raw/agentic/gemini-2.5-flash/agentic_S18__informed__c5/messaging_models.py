from typing import Optional, Any
from dataclasses import dataclass

@dataclass
class MessagePayload:
    id: str
    type: str
    data: dict
    attributes: Optional[dict] = None

@dataclass
class ConsumedMessage:
    message_id: str
    payload: MessagePayload
    received_at: str
    raw_message: Any # Raw provider message object

@dataclass
class ProcessedMessageResult:
    message_id: str
    status: str # e.g., 'SUCCESS', 'FAILED', 'DEAD_LETTERED'
    processed_data: Optional[dict] = None
    errors: Optional[list[str]] = None

