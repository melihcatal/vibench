from pydantic import BaseModel
from typing import Dict, Optional


class MessagePayload(BaseModel):
    customer_name: str
    order_id: str
    message: str


class MessageEvent(BaseModel):
    event_id: str
    timestamp: str
    payload: MessagePayload
    attributes: Optional[Dict[str, str]] = None


class ProcessedRecord(BaseModel):
    event_id: str
    original_message: str
    summary: Optional[str] = None
    safety_score: Optional[float] = None
    translated_message: Optional[str] = None
    processing_timestamp: Optional[str] = None
