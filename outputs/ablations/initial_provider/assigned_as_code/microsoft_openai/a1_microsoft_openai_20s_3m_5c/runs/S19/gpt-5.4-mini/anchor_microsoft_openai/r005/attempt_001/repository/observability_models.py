from datetime import datetime, timezone


def to_utc_timestamp(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.timestamp()
    return float(value)


def normalize_points(points):
    return sorted(
        [{'timestamp': to_utc_timestamp(point['timestamp']), 'value': float(point['value'])} for point in points],
        key=lambda point: point['timestamp'],
    )


def summarize_values(values):
    values = [float(value) for value in values]
    if not values:
        return {'count': 0, 'min': None, 'max': None, 'average': None}
    return {'count': len(values), 'min': min(values), 'max': max(values), 'average': sum(values) / len(values)}
