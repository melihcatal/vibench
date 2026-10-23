import json
from datetime import datetime, timezone


def normalize_timestamp_ms(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        text = value.strip()
        if text.isdigit():
            return int(text)
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return int(parsed.timestamp() * 1000)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return int(value.timestamp() * 1000)
    raise TypeError("Unsupported timestamp value")


def normalize_log_event(event, default_severity="INFO"):
    normalized = dict(event or {})
    normalized["timestamp_ms"] = normalize_timestamp_ms(normalized.get("timestamp_ms"))
    normalized["severity"] = normalized.get("severity") or default_severity
    return normalized


def encode_log_message(event):
    return json.dumps(normalize_log_event(event), separators=(",", ":"), sort_keys=True)
