import json

def normalize_message_payload(data):
    # Basic normalization for a dictionary payload
    if isinstance(data, dict):
        return json.dumps(data).encode("utf-8")
    elif isinstance(data, str):
        return data.encode("utf-8")
    else:
        return str(data).encode("utf-8")

def parse_message_payload(message_data):
    try:
        return json.loads(message_data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return message_data.decode("utf-8", errors="ignore")

class PubSubMessage:
    def __init__(self, data, attributes=None):
        self.data = data
        self.attributes = attributes if attributes is not None else {}

    def to_publish_format(self):
        return {
            "data": self.data,
            "attributes": self.attributes
        }

    @classmethod
    def from_pubsub_message(cls, message):
        return cls(data=message.data, attributes=dict(message.attributes))
