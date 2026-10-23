import json


def load_json_payload(payload):
    if isinstance(payload, str):
        return json.loads(payload)
    return payload


def normalize_event_payload(payload):
    data = load_json_payload(payload)
    if isinstance(data, dict) and "event" in data:
        return data["event"]
    return data


def normalize_attributes(attributes):
    attributes = attributes or {}
    return {str(key): str(value) for key, value in attributes.items()}


def build_message_record(message_id=None, payload=None, attributes=None, status=None):
    return {
        "message_id": message_id,
        "payload": payload,
        "attributes": normalize_attributes(attributes),
        "status": status,
    }
