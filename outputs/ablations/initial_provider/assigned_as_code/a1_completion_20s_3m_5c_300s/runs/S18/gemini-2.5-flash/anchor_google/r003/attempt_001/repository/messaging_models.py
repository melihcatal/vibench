import json


def normalize_message_payload(data):
    # Basic normalization, can be extended as needed
    if isinstance(data, dict):
        return json.dumps(data).encode("utf-8")
    elif isinstance(data, str):
        return data.encode("utf-8")
    else:
        return str(data).encode("utf-8")


def parse_message_payload(message_data):
    # Decode and parse JSON messages
    try:
        return json.loads(message_data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return message_data.decode("utf-8")


class PubsubMessage:
    def __init__(self, data, attributes=None, message_id=None):
        self.data = data
        self.attributes = attributes or {}
        self.message_id = message_id

    def to_dict(self):
        return {
            "data": self.data.decode("utf-8") if isinstance(self.data, bytes) else self.data,
            "attributes": self.attributes,
            "message_id": self.message_id
        }
