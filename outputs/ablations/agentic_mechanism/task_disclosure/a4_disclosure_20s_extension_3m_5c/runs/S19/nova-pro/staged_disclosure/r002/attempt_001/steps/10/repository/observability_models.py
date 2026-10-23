from typing import Any, Dict, List

def create_request(metric_name: str, dimensions: Dict[str, str], value: float, timestamp: int) -> Dict[str, Any]:
    return {
        'MetricName': metric_name,
        'Dimensions': dimensions,
        'Value': value,
        'Timestamp': timestamp
    }

def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    if 'Metrics' in response:
        return response['Metrics'][0]
    return {}

def normalize_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized_data = []
    for item in data:
        normalized_item = {
            'MetricName': item.get('MetricName', ''),
            'Dimensions': item.get('Dimensions', {}),
            'Value': item.get('Value', 0.0),
            'Timestamp': item.get('Timestamp', 0)
        }
        normalized_data.append(normalized_item)
    return normalized_data