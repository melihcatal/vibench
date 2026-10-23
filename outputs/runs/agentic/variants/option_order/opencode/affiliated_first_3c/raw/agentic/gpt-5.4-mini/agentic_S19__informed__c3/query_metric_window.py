from datetime import datetime
from typing import Dict, List, Optional

from observability_client import ObservabilityClientFactory
from observability_models import MetricWindowRequest, normalize_dimensions, series_from_datapoints


def query_metric_window(metric_name: str, namespace: str, start_time: datetime, end_time: datetime, period: int = 60, dimensions: Optional[Dict[str, str]] = None) -> List[dict]:
    factory = ObservabilityClientFactory()
    request = MetricWindowRequest(namespace=namespace, metric_name=metric_name, start_time=start_time, end_time=end_time, period=period, dimensions=dimensions)
    client = factory.cloudwatch()
    response = client.get_metric_statistics(Namespace=request.namespace, MetricName=request.metric_name, StartTime=request.start_time, EndTime=request.end_time, Period=request.period, Statistics=['Average'], Dimensions=normalize_dimensions(request.dimensions))
    series = series_from_datapoints(metric_name=request.metric_name, namespace=request.namespace, datapoints=response.get('Datapoints', []))
    return [{'timestamp': point.timestamp, 'value': point.value} for point in sorted(series.points, key=lambda p: p.timestamp)]
