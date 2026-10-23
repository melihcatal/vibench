from typing import Any, Dict, List


def normalize_metric_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'metric': payload['metric'],
        'start_time': int(payload['start_time']),
        'end_time': int(payload['end_time']),
        'dimensions': {k: v for k, v in payload['dimensions'].items()}
    }


def normalize_metric_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [{'timestamp': p['Timestamp'].timestamp(), 'value': float(p['Average'])} for p in response['Datapoints']]