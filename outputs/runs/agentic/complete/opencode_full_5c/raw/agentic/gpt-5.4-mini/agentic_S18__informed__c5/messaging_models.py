from dataclasses import dataclass, field
from typing import Any

@dataclass
class MessageEnvelope:
    payload: Any
    attributes: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    message_id: str | None = None
    def to_dict(self):
        body = {'payload': self.payload, 'attributes': self.attributes, 'metadata': self.metadata}
        if self.message_id is not None:
            body['message_id'] = self.message_id
        return body

def normalize_attributes(attributes):
    if not attributes:
        return {}
    return {str(k): str(v) for k, v in attributes.items()}

def normalize_batch_payloads(messages):
    normalized = []
    for item in messages:
        if isinstance(item, dict):
            normalized.append({'id': item.get('id'), 'payload': item.get('payload'), 'attributes': item.get('attributes', {})})
        else:
            normalized.append({'id': None, 'payload': item, 'attributes': {}})
    return normalized

def normalize_received_message(received):
    data = received.message.data.decode('utf-8')
    attrs = dict(received.message.attributes)
    return {'message_id': received.message.message_id, 'data': data, 'attributes': attrs}

def build_publish_result(**kwargs): return kwargs
def build_consume_result(**kwargs): return kwargs
def build_dead_letter_result(**kwargs): return kwargs
def build_batch_result(**kwargs): return kwargs
