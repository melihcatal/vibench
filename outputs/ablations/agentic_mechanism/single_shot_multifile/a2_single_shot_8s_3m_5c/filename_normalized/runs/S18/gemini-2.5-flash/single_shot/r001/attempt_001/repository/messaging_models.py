from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

@dataclass
class MessagePayload:
    id: str
    content: Dict[str, Any]
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConsumedMessage:
    body: Dict[str, Any]
    receipt_handle: str
    message_id: str

@dataclass
class AuditRecord:
    message_id: str
    original_payload: Dict[str, Any]
    processed_payload: Optional[Dict[str, Any]] = None
    processing_summary: Optional[str] = None
    translation_status: Optional[str] = None
    safety_check_result: Optional[Dict[str, Any]] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())