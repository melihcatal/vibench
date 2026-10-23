import json


def _get(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def normalize_time_range(params):
    start = _get(params, "start_time") or _get(params, "start_time_ms")
    end = _get(params, "end_time") or _get(params, "end_time_ms")
    if start is None or end is None:
        raise ValueError("start_time and end_time are required")
    return int(start), int(end)


def normalize_log_event(event):
    if isinstance(event, str):
        try:
            event = json.loads(event)
        except Exception:
            return {"message": event}
    if not isinstance(event, dict):
        raise TypeError("log event must be a dict or JSON string")
    normalized = dict(event)
    if "severity" not in normalized and "level" in normalized:
        normalized["severity"] = normalized["level"]
    if "message" not in normalized:
        normalized["message"] = json.dumps(normalized, sort_keys=True)
    return normalized


def build_filter_clause(filters):
    if not filters:
        return ""
    parts = []
    for key, value in filters.items():
        if value is None:
            continue
        if isinstance(value, (int, float)):
            parts.append(f'{key}={value}')
        else:
            safe = str(value).replace("'", "\\'")
            parts.append(f"{key}='{safe}'")
    return " AND ".join(parts)
