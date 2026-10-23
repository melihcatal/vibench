from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Dict

class MessagePayload(BaseModel):
    event_id: str = Field(..., description="Unique identifier for the event")
    timestamp: datetime = Field(..., description="ISO 8601 timestamp when the event occurred")
    data: Dict[str, Any] = Field({}, description="Arbitrary event payload")
    # Optional attributes that you may want to expose
    user_id: str = None
    source: str = None

def normalize_payload(raw_event: dict) -> MessagePayload:
    """Convert raw JSON dict to MessagePayload, ensuring required fields are present."""
    # Ensure timestamp is a datetime object
    ts = raw_event.get('timestamp')
    if ts:
        # Accept ISO string or epoch int/float
        try:
            ts = datetime.fromisoformat(ts.rstrip('Z')).replace(tzinfo=datetime.timezone.utc)
        except Exception:
            # fallback to POSIX timestamp
            try:
                ts = datetime.utcfromtimestamp(float(ts))
            except Exception:
                raise ValueError('Invalid timestamp format')
        raw_event['timestamp'] = ts
    return MessagePayload(**raw_event)

# Example helper to flatten nested structures for simpler storage

def flatten(event: MessagePayload) -> dict:
    """Flatten a MessagePayload into a flat dict suitable for DB storage."""
    flat = {
        'event_id': event.event_id,
        'timestamp': event.timestamp.isoformat(),
        **event.data
    }
    if event.user_id:
        flat['user_id'] = event.user_id
    if event.source:
        flat['source'] = event.source
    return flat

# Example usage (local test)
if __name__ == '__main__':
    sample = {
        'event_id': 'demo-001',
        'timestamp': '2025-08-14T12:34:56Z',
        'data': {'key': 'value'}
    }
    payload = normalize_payload(sample)
    print('Normalized payload:', payload)
    print('Flattened:', flatten(payload))
