from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
import uuid

@dataclass
class EventMessage:
    """Represents a generic event message payload."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    timestamp: str = field(default_factory=lambda: "") # ISO format
    source: str = "your-service-name"
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

@dataclass
class BatchEventEntry:
    """Represents an entry for batch publishing."""
    Id: str # Must match the 'Id' key required by SNS/SQS batch operations
    Message: str # JSON string of the event payload
    MessageStructure: str = 'json'
    MessageAttributes: Optional[Dict[str, Dict[str, str]]] = None # For SQS/SNS

@dataclass
class ConsumedMessage:
    """Represents a message consumed from a queue."""
    message_id: str
    receipt_handle: str
    body: Dict[str, Any] # Parsed JSON body
    attributes: Optional[Dict[str, str]] = None

@dataclass
class AuditRecord:
    """Represents a record to be stored in an audit log (e.g., DynamoDB)."""
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_id: str
    timestamp: str
    status: str # e.g., 'PROCESSED', 'FAILED', 'DEAD_LETTERED'
    service_name: str = "your-processor-service"
    details: Optional[Dict[str, Any]] = None

@dataclass
class TranslationRequest:
    """Represents a request for text translation."""
    text: str
    source_language_code: str
    target_language_code: str

@dataclass
class SafetyCheckRequest:
    """Represents a request for content safety check."""
    text: str
    language_code: str

@dataclass
class SummaryRequest:
    """Represents a request for message summarization/key phrase extraction."""
    text: str
    language_code: str
