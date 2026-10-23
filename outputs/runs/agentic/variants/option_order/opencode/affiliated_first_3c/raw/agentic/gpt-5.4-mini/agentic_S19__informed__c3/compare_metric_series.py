from datetime import datetime
from typing import Dict, Optional

from observability_client import ObservabilityClientFactory
from observability_models import normalize_dimensions


def compare_metric_series(metric_name: str, namespace: str, start_time: datetime, end_time: datetime, left_dimensions: Optional[Dict[str, str]] = None, right_dimensions: Optional[Dict[str, str]] = None) -> Dict[str, list]:
    client = ObservabilityClientFactory().cloudwatch()
    left = client.get_metric_statistics(Namespace=namespace, MetricName=metric_name, StartTime=start_time, EndTime=end_time, Period=60, Statistics=['Average'], Dimensions=normalize_dimensions(left_dimensions))
    right = client.get_metric_statistics(Namespace=namespace, MetricName=metric_name, StartTime=start_time, EndTime=end_time, Period=60, Statistics=['Average'], Dimensions=normalize_dimensions(right_dimensions))
    return {'left': [{'timestamp': dp.get('Timestamp'), 'value': float(dp.get('Average', 0.0))} for dp in left.get('Datapoints', [])], 'right': [{'timestamp': dp.get('Timestamp'), 'value': float(dp.get('Average', 0.0))} for dp in right.get('Datapoints', [])]}
