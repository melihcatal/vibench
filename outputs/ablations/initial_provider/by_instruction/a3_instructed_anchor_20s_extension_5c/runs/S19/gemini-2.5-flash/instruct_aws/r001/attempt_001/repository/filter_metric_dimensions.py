from datetime import datetime, timedelta
from typing import List, Dict, Optional

from observability_client import ObservabilityClient
from observability_models import MetricQueryResult, MetricDatapoint

def filter_metric_dimensions(metric_name: str, namespace: str, duration_minutes: int, period_seconds: int, statistics: List[str], filter_dimensions: Dict[str, str]) -> MetricQueryResult:
    client = ObservabilityClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)

    datapoints_raw = client.get_metric_data(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        statistics=statistics,
        dimensions=filter_dimensions
    )

    datapoints = []
    for dp in datapoints_raw:
        value = dp.get(statistics[0]) if statistics else None
        if value is not None:
            datapoints.append(MetricDatapoint(timestamp=dp['Timestamp'], value=float(value), unit=dp.get('Unit')))

    return MetricQueryResult(metric_name=metric_name, namespace=namespace, datapoints=datapoints, dimensions=filter_dimensions)
