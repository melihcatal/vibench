import json

def normalize_event(event: dict) -> dict:
    """Validate and normalize an incoming event.

    Ensures the payload is JSON‑serializable and adds a timestamp.
    """
    if not isinstance(event, dict):
        raise ValueError("Event must be a dict")
    # Add processing timestamp
    event.setdefault('processed_at', None)
    try:
        json.dumps(event)  # simple validation
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Event not JSON‑serializable: {exc}")
    return event

def normalize_message(message: dict) -> dict:
    """Normalize an inbound message payload.

    By default returns the payload unchanged; subclasses can override.
    """
    return message

def prepare_dead_letter(original: dict, error_details: str) -> dict:
    """Prepare a normalized dead‑letter record.

    Includes the original payload and error context.
    """
    dl = {
        'original_payload': original,
        'error': error_details,
        'dead_lettered_at': None
    }
    dl.setdefault('dead_lettered_at', None)
    try:
        json.dumps(dl)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"DL payload not JSON‑serializable: {exc}")
    return dl
