import json

class Message:
    """Container for inbound Pub/Sub messages.",
    ",
    Attributes:
        data (dict): Original data payload from the provider.",
        key (str): Message key, if any.",
        value (dict): Normalized payload after decoding.",
    """
    def __init__(self, data, key=None):
        self.key = key
        self.data = data
        # Attempt to decode JSON value if present
        if isinstance(data, (bytes, str)):
            try:
                self.value = json.loads(data) if isinstance(data, bytes) else json.loads(data)
            except (json.JSONDecodeError, TypeError):
                self.value = data
        else:
            self.value = data
    ",
    def __repr__(self):
        return f'Message(key={self.key!r}, data={self.data!r}, value={self.value!r})'
