from typing import Dict, List


def normalize_metric_payload(payload: Dict) -> Dict:
    normalized = {
        'start_time': payload.get('start_time', None),
        'end_time': payload.get('end_time', None),
        'metric': payload.get('metric', None),
        'filter': payload.get('filter', None),
        'filter1': payload.get('filter1', None),
        'filter2': payload.get('filter2', None)
    }
    return {k: v for k, v in normalized.items() if v is not None}


def parse_metric_response(response: Dict) -> Dict:
    points = [{'timestamp': point['timestamp'], 'value': point['value']} for point in response.get('points', []) if point['value'] is not None]
    return {'points': sorted(points, key=lambda point: point['timestamp'])}


def parse_metric_comparison_response(response: Dict) -> Dict:
    series1 = [{'timestamp': point['timestamp'], 'value': point['value']} for point in response.get('series1', []) if point['value'] is not None]
    series2 = [{'timestamp': point['timestamp'], 'value': point['value']} for point in response.get('series2', []) if point['value'] is not None]
    return {'series1': sorted(series1, key=lambda point: point['timestamp']), 'series2': sorted(series2, key=lambda point: point['timestamp'])}