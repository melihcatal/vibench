from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class Event:
    """
    Represents a Pub/Sub event with data and attributes.
    """

    data: Dict[str, Any]
    attributes: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the event to a dictionary.
        """
        return {
            "data": self.data,
            "attributes": self.attributes,
        }


@dataclass
class BatchEvent:
    """
    Represents a batch Pub/Sub event with data and optional attributes.
    """

    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

        # Ensure each event has a unique identifier
        if "event_id" not in self.attributes:
            import uuid

            self.attributes["event_id"] = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the batch event to a dictionary.
        """
        return {
            "data": self.data,
            "attributes": self.attributes,
        }
