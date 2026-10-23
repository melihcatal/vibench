import json


def load_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, str):
        return json.loads(payload)
    return dict(payload)


def normalize_message(message):
    if message is None:
        return {}
    if isinstance(message, dict):
        data = dict(message)
    else:
        data = {"data": message}
    if isinstance(data.get("data"), (bytes, bytearray)):
        data["data"] = data["data"].decode("utf-8")
    return data


def encode_json(value):
    return json.dumps(value, separators=(",", ":")).encode("utf-8")


def decode_json(value):
    if value is None:
        return None
    if isinstance(value, (bytes, bytearray)):
        return json.loads(value.decode("utf-8"))
    if isinstance(value, str):
        return json.loads(value)
    return value
