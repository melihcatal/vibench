from datetime import datetime, timezone


def timestamp_to_epoch(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).timestamp()
    return datetime.fromisoformat(value).astimezone(timezone.utc).timestamp()


def normalize_points(result):
    points = []
    for metric in getattr(result, 'metrics', []):
        for series in getattr(metric, 'timeseries', []):
            for point in getattr(series, 'data', []):
                for attr in ('average', 'total', 'maximum', 'minimum', 'count'):
                    value = getattr(point, attr, None)
                    if value is not None:
                        points.append({'timestamp': point.timestamp.timestamp(), 'value': float(value), 'stat': attr})
                        break
    return sorted(points, key=lambda item: item['timestamp'])


def metric_window_response(points, **extra):
    payload = {'points': points}
    payload.update(extra)
    return payload
