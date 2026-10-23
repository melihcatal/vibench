import base64
from datetime import datetime, timezone


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def build_event_payload(payload):
    if payload is None:
        return {"type": "event", "created_at": _now_iso()}
    if isinstance(payload, dict):
        normalized = dict(payload)
        normalized.setdefault("created_at", _now_iso())
        return normalized
    return {"type": "event", "created_at": _now_iso(), "payload": payload}


def build_dead_letter_payload(payload):
    if isinstance(payload, dict):
        normalized = dict(payload)
        normalized["dead_lettered_at"] = _now_iso()
        return normalized
    return {"payload": payload, "dead_lettered_at": _now_iso()}


def build_batch_messages(messages):
    if not isinstance(messages, list):
        raise ValueError("messages must be a list")
    batch = []
    for index, message in enumerate(messages):
        if isinstance(message, dict):
            payload = message.get("payload", message)
            msg_id = message.get("id", str(index))
            attributes = message.get("attributes", {})
        else:
            payload = message
            msg_id = str(index)
            attributes = {}
        batch.append({"id": str(msg_id), "payload": payload, "attributes": attributes})
    return batch


def normalize_attributes(attributes):
    if not attributes:
        return {}
    normalized = {}
    for key, value in dict(attributes).items():
        normalized[str(key)] = str(value)
    return normalized


def decode_pubsub_message(message):
    data = message.data or b""
    try:
        decoded = data.decode("utf-8")
    except Exception:
        decoded = base64.b64encode(data).decode("ascii")
    result = {"data": decoded, "message_id": getattr(message, "message_id", None), "attributes": dict(getattr(message, "attributes", {}) or {})}
    return result


def success_result(**kwargs):
    payload = dict(kwargs)
    payload.setdefault("status", "ok")
    payload.setdefault("processed_at", _now_iso())
    return payload
