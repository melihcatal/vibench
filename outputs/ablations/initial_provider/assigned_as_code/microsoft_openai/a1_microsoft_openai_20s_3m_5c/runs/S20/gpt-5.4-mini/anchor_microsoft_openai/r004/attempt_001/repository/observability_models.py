from datetime import datetime, timezone


def normalize_timestamp_ms(timestamp_ms):
    if timestamp_ms is None:
        timestamp_ms = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    return int(timestamp_ms)


def to_iso_timestamp(timestamp_ms):
    return datetime.fromtimestamp(normalize_timestamp_ms(timestamp_ms) / 1000, tz=timezone.utc).isoformat()


def build_log_event(payload, timestamp_field="TimeGenerated"):
    event = dict(payload)
    event[timestamp_field] = to_iso_timestamp(event.pop("timestamp_ms", None))
    return event


def build_correlation_event(payload, correlation_id_field="correlation_id"):
    event = dict(payload)
    if correlation_id_field not in event:
        raise KeyError(correlation_id_field)
    event[correlation_id_field] = str(event[correlation_id_field])
    return event


def coerce_rows(rows):
    return [dict(row) for row in rows]
