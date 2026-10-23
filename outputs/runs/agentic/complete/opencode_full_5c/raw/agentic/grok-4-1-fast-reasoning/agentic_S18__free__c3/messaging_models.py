from dataclasses import dataclass
from typing import Dict, Any, Optional
import json


@dataclass
class PubSubMessage:
    message_id: str
    data: bytes
    attributes: Dict[str, str]
    publish_time: str
    ack_id: Optional[str] = None

    @property
    def payload(self) -> Dict[str, Any]:
        return json.loads(self.data.decode("utf-8"))
