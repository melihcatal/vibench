import json
from typing import Any, Dict

def normalize_event_payload(payload: Dict[str, Any]) -> bytes:
    """Normalizes a dictionary payload to bytes for Pub/Sub."""
    return json.dumps(payload).encode("utf-8")

def parse_pubsub_message(message_data: bytes) -> Dict[str, Any]:
    """Parses Pub/Sub message data (bytes) back into a dictionary."""
    return json.loads(message_data.decode("utf-8"))
