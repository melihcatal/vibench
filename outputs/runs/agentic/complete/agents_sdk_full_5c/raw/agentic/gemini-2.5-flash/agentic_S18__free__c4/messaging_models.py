from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class EventMessage:
    """Represents a standardized event message structure."""
    id: str
    type: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    source: Optional[str] = None
    timestamp: Optional[str] = None # ISO 8601 format

@dataclass
class ConsumedMessage:
    """Represents a message consumed from a queue."""
    receipt_handle: str
    message_id: str
    body: Dict[str, Any]
    attributes: Dict[str, str]

@dataclass
class DeadLetterMessage:
    """Represents a message sent to a dead-letter queue."""
    original_message_id: Optional[str]
    error_details: str
    original_payload: Dict[str, Any]

@dataclass
class BatchPublishEntry:
    """Represents an entry for batch publishing."""
    id: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

if __name__ == "__main__":
    # Example Usage
    # event = EventMessage(id="evt1", type="user_created", payload={"name": "John Doe"})
    # print(event)
    # consumed = ConsumedMessage(receipt_handle="abc", message_id="msg1", body={"key": "value"}, attributes={"sender": "serviceX"})
    # print(consumed)
    pass
