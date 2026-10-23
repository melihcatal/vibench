import json

def create_event_payload(data: dict, event_type: str) -> str:
    payload = {
        "event_type": event_type,
        "data": data
    }
    return json.dumps(payload)
