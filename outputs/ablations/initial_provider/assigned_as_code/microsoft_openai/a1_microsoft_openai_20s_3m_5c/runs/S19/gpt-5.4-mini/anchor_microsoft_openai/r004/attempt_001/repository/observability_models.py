from datetime import datetime, timezone


def parse_timestamp(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def normalize_window(payload):
    start = parse_timestamp(payload['start_time'])
    end = parse_timestamp(payload['end_time'])
    return start, end


def normalize_dimensions(payload):
    dimensions = payload.get('dimensions') or payload.get('filters') or {}
    if isinstance(dimensions, dict):
        return {str(key): str(value) for key, value in dimensions.items()}
    return {str(item.get('name')): str(item.get('value')) for item in dimensions if item.get('name') is not None}


def metric_points(result):
    points = []
    for metric in getattr(result, 'metrics', []):
        for series in getattr(metric, 'timeseries', []):
            for point in getattr(series, 'data', []):
                timestamp = getattr(point, 'timestamp', None)
                if timestamp is None:
                    continue
                value = next((getattr(point, name) for name in ('average', 'minimum', 'maximum', 'total', 'count') if getattr(point, name, None) is not None), None)
                if value is None:
                    continue
                points.append({'timestamp': timestamp.timestamp(), 'value': float(value)})
    return sorted(points, key=lambda point: point['timestamp'])


def summarize_points(points):
    values = [point['value'] for point in points]
    if not values:
        return {'count': 0, 'minimum': None, 'maximum': None, 'average': None}
    return {'count': len(values), 'minimum': min(values), 'maximum': max(values), 'average': sum(values) / len(values)}
