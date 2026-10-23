import json


def normalize_log_event(event, default_severity=None, correlation_id=None):
    normalized = dict(event or {})
    if default_severity and "severity" not in normalized:
        normalized["severity"] = default_severity
    if correlation_id and "correlation_id" not in normalized:
        normalized["correlation_id"] = correlation_id
    return normalized


def serialize_message(payload):
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def parse_cw_log_event(event):
    message = event.get("message")
    try:
        parsed = json.loads(message)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    return {"message": message, "timestamp": event.get("timestamp")}
