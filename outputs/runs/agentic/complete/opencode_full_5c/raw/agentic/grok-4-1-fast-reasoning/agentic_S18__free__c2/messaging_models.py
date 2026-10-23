from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import json


@dataclass
class PubSubMessage:
    data: bytes
    message_id: str = ""
    attributes: Dict[str, str] = field(default_factory=dict)
    publish_time: str = ""
    ack_id: str = ""

    def payload(self) -> Dict[str, Any]:
        return json.loads(self.data.decode("utf-8"))

    @classmethod
    def from_dict(
        cls, d: Dict[str, Any], attributes: Dict[str, str] = None
    ) -> "PubSubMessage":
        if attributes is None:
            attributes = {}
        return cls(data=json.dumps(d).encode("utf-8"), attributes=attributes)
