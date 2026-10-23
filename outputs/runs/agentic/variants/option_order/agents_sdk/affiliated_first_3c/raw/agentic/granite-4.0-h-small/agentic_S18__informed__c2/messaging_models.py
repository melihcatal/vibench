import json

class Message:
    """Normalization wrapper for Pub/Sub messages."""
    def __init__(self, raw):
        self.raw = raw
        # Decode payload if present
        self.payload = json.loads(raw['data'].decode('utf-8')) if raw.get('data') else {}
        self.attributes = raw.get('attributes', {})
        self.message_id = raw.get('message_id')
        self.publish_time = raw.get('publish_time')

    def to_dict(self):
        return {
            'payload': self.payload,
            'attributes': self.attributes,
            'message_id': self.message_id,
            'publish_time': str(self.publish_time)
        }

# Example schema validation helpers (could use pydantic for stricter validation)
def validate_event_schema(event: dict):
    """Placeholder for event schema validation logic."""
    required_fields = {'event_type', 'user_id', 'timestamp'}
    missing = required_fields - event.keys()
    if missing:
        raise ValueError(f'Missing required fields: {missing}')

def normalize_payload(raw_message: dict) -> dict:
    """Convert a raw Pub/Sub dict to a normalized Message object."""
    return Message(raw_message).to_dict()
