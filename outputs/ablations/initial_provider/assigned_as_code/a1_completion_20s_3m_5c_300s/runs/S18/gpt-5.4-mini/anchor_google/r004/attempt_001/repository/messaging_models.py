import json


def normalize_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except Exception:
            return {"text": payload}
    return dict(payload)


def build_message_data(payload):
    normalized = normalize_payload(payload)
    if "event" in normalized:
        normalized = normalized["event"]
    return json.dumps(normalized).encode("utf-8")


def parse_pubsub_message(message):
    data = getattr(message, "data", b"")
    attributes = dict(getattr(message, "attributes", {}) or {})
    text = data.decode("utf-8") if isinstance(data, (bytes, bytearray)) else str(data)
    try:
        parsed = json.loads(text)
    except Exception:
        parsed = {"text": text}
    return {"data": parsed, "attributes": attributes, "message_id": getattr(message, "message_id", None)}
