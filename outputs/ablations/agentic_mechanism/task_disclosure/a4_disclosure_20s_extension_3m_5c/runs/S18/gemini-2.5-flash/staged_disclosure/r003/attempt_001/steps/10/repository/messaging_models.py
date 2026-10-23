
"""
Local request, response, and normalization helpers for Pub/Sub Messaging.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

@dataclass
class PubsubMessage:
    """Represents a single Pub/Sub message."""
    data: Optional[bytes] = None
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: Optional[str] = None
    publish_time: Optional[str] = None

@dataclass
class PubsubRequest:
    """Represents a request to publish one or more Pub/Sub messages."""
    messages: List[PubsubMessage]

@dataclass
class PubsubResponse:
    """Represents a response from a Pub/Sub publish operation."""
    message_ids: List[str]

def normalize_message_data(data: Any) -> bytes:
    """Normalizes various data types to bytes for Pub/Sub message data."""
    if isinstance(data, bytes):
        return data
    elif isinstance(data, str):
        return data.encode('utf-8')
    elif data is None:
        return b''
    else:
        # For other types, convert to string representation then to bytes
        return str(data).encode('utf-8')

def parse_pubsub_message(message_data: Dict[str, Any]) -> PubsubMessage:
    """Parses a dictionary (e.g., from a Pub/Sub push subscription) into a PubsubMessage object."""
    return PubsubMessage(
        data=message_data.get('data'),
        attributes=message_data.get('attributes', {}),
        message_id=message_data.get('messageId'),
        publish_time=message_data.get('publishTime')
    )
