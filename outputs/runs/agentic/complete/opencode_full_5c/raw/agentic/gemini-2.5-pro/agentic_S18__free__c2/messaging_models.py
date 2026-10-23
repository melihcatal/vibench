from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Message:
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    message_id: Optional[str] = None


@dataclass
class ReceivedMessage:
    ack_id: str
    message: Message
    delivery_attempt: int


@dataclass
class ProcessingResult:
    message_id: str
    status: str
    error_message: Optional[str] = None
