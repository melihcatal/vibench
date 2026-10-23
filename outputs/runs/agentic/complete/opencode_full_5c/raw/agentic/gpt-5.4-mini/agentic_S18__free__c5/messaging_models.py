import json
from dataclasses import dataclass


def normalize_attributes(attributes=None):
    attributes = attributes or {}
    return {str(k): str(v) for k, v in attributes.items()}


def normalize_payload_text(value):
    if isinstance(value, dict) and 'text' in value:
        return str(value['text'])
    return str(value)


def serialize_event(event):
    return json.dumps(event, separators=(',', ':'), sort_keys=True).encode('utf-8')


@dataclass
class PublishRequest:
    event: dict
    attributes: dict

    @classmethod
    def from_payload(cls, payload):
        return cls(event=payload, attributes=payload.get('attributes', {}) if isinstance(payload, dict) else {})


@dataclass
class PublishResult:
    message_id: str
    topic: str
    attributes: dict
    payload: object

    def to_json(self):
        return json.dumps({'message_id': self.message_id, 'topic': self.topic, 'attributes': self.attributes, 'payload': self.payload}, sort_keys=True)


@dataclass
class ConsumeResult:
    message: object | None
    subscription: str

    @classmethod
    def empty(cls, subscription):
        return cls(message=None, subscription=subscription)

    def to_json(self):
        return json.dumps({'message': self.message, 'subscription': self.subscription}, sort_keys=True)


@dataclass
class DeadLetterRequest:
    record: dict
    attributes: dict

    @classmethod
    def from_payload(cls, payload):
        return cls(record=payload, attributes=payload.get('attributes', {}) if isinstance(payload, dict) else {})


@dataclass
class BatchMessage:
    body: dict
    attributes: dict


@dataclass
class BatchPublishRequest:
    messages: list

    @classmethod
    def from_payload(cls, payload):
        messages = [BatchMessage(body=item, attributes=item.get('attributes', {}) if isinstance(item, dict) else {}) for item in payload.get('messages', [])]
        return cls(messages=messages)


@dataclass
class BatchPublishResult:
    message_ids: list
    topic: str

    def to_json(self):
        return json.dumps({'message_ids': self.message_ids, 'topic': self.topic}, sort_keys=True)


def decode_message(message):
    return json.loads(message.data.decode('utf-8'))


def normalize_message_record(record):
    return record
