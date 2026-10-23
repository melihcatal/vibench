from typing import Any, Dict, Mapping, Optional


def _stringify(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _stringify(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_stringify(v) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def normalize_event_payload(event: Mapping[str, Any]) -> Dict[str, Any]:
    payload = dict(event)
    payload.setdefault("event_type", "customer.event")
    payload.setdefault("source", "pubsub")
    return _stringify(payload)


def normalize_consumed_message(data: bytes, attributes: Mapping[str, str]) -> Dict[str, Any]:
    text = data.decode("utf-8") if data else ""
    try:
        body = __import__("json").loads(text) if text else {}
    except Exception:
        body = {"raw_text": text}
    return {"body": _stringify(body), "attributes": dict(attributes)}


def normalize_dead_letter_payload(message: Mapping[str, Any]) -> Dict[str, Any]:
    payload = dict(message)
    payload.setdefault("failure_reason", "processing_failed")
    payload.setdefault("destination", "dead-letter")
    return _stringify(payload)


def normalize_batch_item(item: Mapping[str, Any], index: int) -> Dict[str, Any]:
    payload = dict(item)
    payload.setdefault("item_id", item.get("item_id", index))
    payload.setdefault("batch_index", index)
    payload.setdefault("event_type", "batch.message")
    return _stringify(payload)
