from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import uuid


@dataclass
class Message:
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class ProcessedMessage:
    original_message: Message
    status: str
    processed_at: str
    summary: Optional[str] = None
    is_safe: Optional[bool] = None
    translation: Optional[str] = None
    audit_id: Optional[str] = None


@dataclass
class BatchPublishRequest:
    messages: List[Message]
