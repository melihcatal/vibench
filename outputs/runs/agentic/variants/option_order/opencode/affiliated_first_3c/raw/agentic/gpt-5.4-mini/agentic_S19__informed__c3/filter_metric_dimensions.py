from datetime import datetime
from typing import Dict, List, Optional

from observability_client import ObservabilityClientFactory
from observability_models import normalize_dimensions


def filter_metric_dimensions(metric_name: str, namespace: str, start_time: datetime, end_time: datetime, dimensions: Optional[Dict[str, str]] = None) -> List[dict]:
    client = ObservabilityClientFactory().cloudwatch()
    response = client.get_metric_statistics(Namespace=namespace, MetricName=metric_name, StartTime=start_time, EndTime=end_time, Period=60, Statistics=['Average'], Dimensions=normalize_dimensions(dimensions))
    return [{'timestamp': dp.get('Timestamp'), 'value': float(dp.get('Average', 0.0)), 'dimensions': dimensions or {}} for dp in response.get('Datapoints', [])]
