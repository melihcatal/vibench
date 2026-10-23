from datetime import datetime, timezone


def normalize_timestamp_ms(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return int(value.replace(tzinfo=timezone.utc).timestamp() * 1000)
    return int(value)


def build_event(message, severity, **fields):
    event = {"message": message, "severity": severity}
    event.update(fields)
    return event


def to_filters(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}
