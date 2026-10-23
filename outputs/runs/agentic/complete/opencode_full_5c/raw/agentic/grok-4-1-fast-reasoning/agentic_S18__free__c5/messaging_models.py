from dataclasses import dataclass
from typing import Dict, Any, Optional
import json


@dataclass
class PubSubMessage:
    message_id: str
    data: str
    attributes: Dict[str, str] = None
    ordering_key: Optional[str] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PubSubMessage":
        return cls(
            message_id=d["message_id"],
            data=d["data"],
            attributes=d.get("attributes", {}),
            ordering_key=d.get("ordering_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "data": self.data,
            "attributes": self.attributes or {},
            "ordering_key": self.ordering_key,
        }
