from typing import Any, Dict, List

import boto3

cloudwatch = boto3.client('cloudwatch')


def create_metric_request(namespace: str, metric_name: str, dimensions: List[Dict[str, str]], statistic: str, period: int, start_time: str, end_time: str) -> Dict[str, Any]:
    return {
        'Namespace': namespace,
        'MetricName': metric_name,
        'Dimensions': dimensions,
        'Statistics': [statistic],
        'Period': period,
        'StartTime': start_time,
        'EndTime': end_time
    }


def normalize_metric_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    datapoints = response.get('Datapoints', [])
    normalized_data = []
    for datapoint in datapoints:
        normalized_data.append({
            'Timestamp': datapoint['Timestamp'].isoformat(),
            'Value': datapoint['Value']
        })
    return normalized_data
