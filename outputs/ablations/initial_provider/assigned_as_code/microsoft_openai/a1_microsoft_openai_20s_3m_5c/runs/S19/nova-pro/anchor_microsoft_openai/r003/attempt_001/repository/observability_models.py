from typing import Any, Dict


def normalize_metric_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in response.items():
        if isinstance(value, list):
            normalized[key] = [normalize_metric_point(point) for point in value]
        else:
            normalized[key] = value
    return normalized


def normalize_metric_point(point: Dict[str, Any]) -> Dict[str, Any]:
    return {'timestamp': point['timestamp'].timestamp(), 'value': float(point['value'])}