from datetime import datetime, timezone


def normalize_time_range(start_time=None, end_time=None, lookback_minutes=60):
    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time.timestamp() - lookback_minutes * 60)
    if hasattr(start_time, "timestamp"):
        start_time = start_time.timestamp()
    if hasattr(end_time, "timestamp"):
        end_time = end_time.timestamp()
    return int(start_time * 1000), int(end_time * 1000)


def build_filter_expression(filters=None, severity=None):
    parts = []
    filters = filters or {}
    for key, value in filters.items():
        parts.append(f'{{ $.{key} = "{value}" }}')
    if severity:
        parts.append(f'{{ $.severity = "{severity}" }}')
    return " && ".join(parts) if parts else None


def parse_log_event(event):
    message = event.get("message", "")
    return {"timestamp": event.get("timestamp"), "message": message}
