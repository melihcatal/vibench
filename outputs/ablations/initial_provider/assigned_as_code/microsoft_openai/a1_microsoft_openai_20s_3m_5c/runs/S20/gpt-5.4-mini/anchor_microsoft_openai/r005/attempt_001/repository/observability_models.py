from datetime import datetime, timezone


def iso_utc(dt):
    if dt is None:
        return None
    if isinstance(dt, (int, float)):
        dt = datetime.fromtimestamp(dt, tz=timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def normalize_time_range(start_time=None, end_time=None, lookback_minutes=None):
    if lookback_minutes is not None and start_time is None and end_time is None:
        end_time = datetime.now(timezone.utc)
        start_time = end_time.timestamp() - (lookback_minutes * 60)
    return {"start_time": iso_utc(start_time), "end_time": iso_utc(end_time)}


def normalize_fields(filters=None):
    filters = filters or {}
    return {k: v for k, v in filters.items() if v is not None}
