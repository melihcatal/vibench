import json


def normalize_message(payload):
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"text": payload}
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


def build_event(event_id, event_type, event, attributes=None):
    return {
        "id": event_id,
        "type": event_type,
        "event": normalize_message(event),
        "attributes": attributes or {},
    }


def build_result(**kwargs):
    return kwargs
