from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Message:
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    message_id: Optional[str] = None


@dataclass
class ProcessedMessage:
    original_message: Message
    status: str
    summary: Optional[str] = None
    is_safe: Optional[bool] = None
    translation: Optional[str] = None
    audit_id: Optional[str] = None
