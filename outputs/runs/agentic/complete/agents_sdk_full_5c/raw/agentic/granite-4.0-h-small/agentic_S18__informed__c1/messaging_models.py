import json
from typing import Any, Dict

def build_event_message(payload: Dict[str, Any], message_id: str = None) -> bytes:
    """Create a JSON encoded payload and optionally assign a Pub/Sub message ID.

    Args:
        payload (Dict[str, Any]): The data to be sent.
        message_id (str, optional): Explicit message ID for Pub/Sub.

    Returns:
        bytes: The serialized payload (UTF-8 string).
    """
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    # Pub/Sub publish API accepts data as bytes; other providers may differ.
    return data

def normalize_message(raw: bytes) -> Dict[str, Any]:
    """Decode a Pub/Sub message payload (bytes) back to a dict.

    Args:
        raw (bytes): The raw message bytes.

    Returns:
        Dict[str, Any]: The normalized Python dictionary.
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {'raw_bytes': raw}
