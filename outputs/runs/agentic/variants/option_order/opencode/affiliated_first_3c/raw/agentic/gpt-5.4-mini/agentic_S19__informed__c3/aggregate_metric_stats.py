from datetime import datetime
from typing import Dict, Optional

from observability_client import ObservabilityClientFactory
from observability_models import MetricWindowRequest, normalize_dimensions


def aggregate_metric_stats(metric_name: str, namespace: str, start_time: datetime, end_time: datetime, period: int = 300, dimensions: Optional[Dict[str, str]] = None) -> Dict[str, float]:
    factory = ObservabilityClientFactory()
    request = MetricWindowRequest(namespace=namespace, metric_name=metric_name, start_time=start_time, end_time=end_time, period=period, dimensions=dimensions)
    client = factory.cloudwatch()
    response = client.get_metric_statistics(Namespace=request.namespace, MetricName=request.metric_name, StartTime=request.start_time, EndTime=request.end_time, Period=request.period, Statistics=['Average', 'Sum', 'Minimum', 'Maximum', 'SampleCount'], Dimensions=normalize_dimensions(request.dimensions))
    datapoints = response.get('Datapoints', [])
    if not datapoints:
        return {'average': 0.0, 'sum': 0.0, 'minimum': 0.0, 'maximum': 0.0, 'sample_count': 0.0}
    latest = sorted(datapoints, key=lambda item: item.get('Timestamp'))[-1]
    return {'average': float(latest.get('Average', 0.0)), 'sum': float(latest.get('Sum', 0.0)), 'minimum': float(latest.get('Minimum', 0.0)), 'maximum': float(latest.get('Maximum', 0.0)), 'sample_count': float(latest.get('SampleCount', 0.0))}
