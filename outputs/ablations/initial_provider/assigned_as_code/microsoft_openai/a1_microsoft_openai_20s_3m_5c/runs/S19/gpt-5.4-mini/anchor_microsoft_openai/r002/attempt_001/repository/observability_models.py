from datetime import datetime, timezone


def to_timestamp(value):
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).timestamp()
    return float(value)


def normalize_points(points):
    return sorted(({'timestamp': to_timestamp(p['timestamp']), 'value': float(p['value'])} for p in points), key=lambda p: p['timestamp'])
