from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SimpleMessage:
    """A simple data class for a message to be published."""
    message_id: str
    data: Dict[str, Any]
