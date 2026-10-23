from datetime import datetime, timezone


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def normalize_attrs(attributes):
    attrs = {}
    for key, value in (attributes or {}).items():
        attrs[str(key)] = "" if value is None else str(value)
    return attrs


def build_event_message(payload, message_id=None):
    body = dict(payload or {})
    body.setdefault("created_at", _now_iso())
    if message_id is not None:
        body["message_id"] = message_id
    return body


def build_dead_letter_message(failed_payload, reason):
    return {"failed_payload": failed_payload, "reason": reason, "dead_lettered_at": _now_iso()}


def normalize_batch_item(item):
    if isinstance(item, dict):
        payload = item.get("payload", item)
        return {"id": item.get("id"), "payload": payload, "attributes": item.get("attributes", {})}
    return {"id": None, "payload": item, "attributes": {}}


def parse_pubsub_message(message):
    data = message.data.decode("utf-8") if getattr(message, "data", None) else ""
    attrs = dict(getattr(message, "attributes", {}) or {})
    return {"data": data, "attributes": attrs, "message_id": getattr(message, "message_id", None), "publish_time": str(getattr(message, "publish_time", ""))}
