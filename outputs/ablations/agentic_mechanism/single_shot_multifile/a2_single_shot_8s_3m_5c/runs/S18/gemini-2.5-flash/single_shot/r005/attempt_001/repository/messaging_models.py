from pydantic import BaseModel
from typing import Any, Optional

class OutgoingMessage(BaseModel):
    message_id: Optional[str] = None
    message_type: str
    payload: Any
    attributes: Optional[dict[str, Any]] = None

class IncomingMessage(BaseModel):
    message_id: str
    receipt_handle: str
    message_type: str
    payload: Any
    attributes: Optional[dict[str, Any]] = None

class ProcessedMessageRecord(BaseModel):
    record_id: str
    original_message_id: str
    processed_timestamp: str
    processing_status: str
    summary: Optional[str] = None
    safety_check_result: Optional[dict] = None
    translated_payload: Optional[dict] = None
    original_payload: Any
