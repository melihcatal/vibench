from dataclasses import dataclass, field


def normalize_attributes(attributes=None):
    if not attributes:
        return {}
    return {str(k): str(v) for k, v in attributes.items() if v is not None}


def normalize_message(message):
    data = getattr(message.message, "data", b"")
    attributes = dict(getattr(message.message, "attributes", {}) or {})
    return {"message_id": getattr(message.message, "message_id", None), "data": data.decode("utf-8") if isinstance(data, (bytes, bytearray)) else data, "attributes": attributes}


@dataclass
class PublishRequest:
    payload: dict
    attributes: dict = field(default_factory=dict)


@dataclass
class PublishResponse:
    message_id: str
    topic_path: str

    def as_dict(self):
        return {"message_id": self.message_id, "topic_path": self.topic_path}


@dataclass
class ConsumeResponse:
    messages: list
    subscription_path: str

    def as_dict(self):
        return {"messages": self.messages, "subscription_path": self.subscription_path}


@dataclass
class DeadLetterRequest:
    payload: dict
    reason: str
    attributes: dict = field(default_factory=dict)

    def as_dict(self):
        return {"payload": self.payload, "reason": self.reason, "attributes": self.attributes}


@dataclass
class BatchPublishRequest:
    messages: list
