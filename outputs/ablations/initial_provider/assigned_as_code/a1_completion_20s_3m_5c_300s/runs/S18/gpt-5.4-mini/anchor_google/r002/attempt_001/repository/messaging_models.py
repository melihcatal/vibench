import json


def load_payload(payload):
    if isinstance(payload, str):
        return json.loads(payload)
    return payload or {}


def normalize_event(payload):
    data = load_payload(payload)
    if isinstance(data, dict) and "event" in data:
        return data["event"]
    return data


def normalize_attributes(attributes):
    return {str(k): str(v) for k, v in (attributes or {}).items()}


def message_record(message_id=None, data=None, attributes=None, metadata=None):
    return {"message_id": message_id, "data": data, "attributes": normalize_attributes(attributes), "metadata": metadata or {}}
