import json
from typing import Dict, Any, Optional, List, TypedDict

class MessagePayload(TypedDict):
    id: str
    text: str
    metadata: Dict[str, Any]

class ConsumedMessage(TypedDict):
    id: str
    receipt_handle: str
    body: Dict[str, Any]
    attributes: Dict[str, Any]

class AuditRecord(TypedDict):
    message_id: str
    status: str
    timestamp: str
    details: Dict[str, Any]

class BatchPublishEntry(TypedDict):
    Id: str
    MessageBody: str
    MessageAttributes: Dict[str, Any]
    MessageGroupId: Optional[str]
    MessageDeduplicationId: Optional[str]
