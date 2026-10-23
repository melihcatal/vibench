
import json
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class PubSubMessage:
    data: Optional[bytes] = None
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: Optional[str] = None
    publish_time: Optional[str] = None

    def to_json(self) -> str:
        payload = {}
        if self.data:
            payload['data'] = self.data.decode('utf-8')
        if self.attributes:
            payload['attributes'] = self.attributes
        if self.message_id:
            payload['messageId'] = self.message_id
        if self.publish_time:
            payload['publishTime'] = self.publish_time
        return json.dumps(payload)

    @classmethod
    def from_json(cls, json_str: str) -> 'PubSubMessage':
        payload = json.loads(json_str)
        data = payload.get('data')
        attributes = payload.get('attributes', {})
        message_id = payload.get('messageId')
        publish_time = payload.get('publishTime')
        return cls(
            data=data.encode('utf-8') if data else None,
            attributes=attributes,
            message_id=message_id,
            publish_time=publish_time
        )

def serialize_message(data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None) -> PubSubMessage:
    """Serializes a dictionary into a PubSubMessage."""
    json_data = json.dumps(data).encode('utf-8')
    return PubSubMessage(data=json_data, attributes=attributes or {})

def deserialize_message(message: PubSubMessage) -> Dict[str, Any]:
    """Deserializes a PubSubMessage data into a dictionary."""
    if message.data:
        return json.loads(message.data.decode('utf-8'))
    return {}
