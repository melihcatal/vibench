import json


def normalize_payload(payload):
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except Exception:
            return {"text": payload}
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


def build_event(message_id, payload, attributes=None):
    event = {"message_id": message_id, "payload": normalize_payload(payload)}
    if attributes:
        event["attributes"] = dict(attributes)
    return event


def parse_message(message):
    if hasattr(message, "message_id"):
        body = getattr(message, "data", b"")
        attrs = getattr(message, "attributes", {})
        return build_event(message.message_id, body, attrs)
    return normalize_payload(message)
