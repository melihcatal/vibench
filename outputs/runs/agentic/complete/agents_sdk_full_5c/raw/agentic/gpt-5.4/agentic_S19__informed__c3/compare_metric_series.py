from __future__ import annotations

from typing import Dict, Optional

from observability_client import get_cloudwatch_client, load_metric_window
from observability_models import MetricComparison


def _query_average(client, metric_name: str, namespace: str, dimensions: Dict[str, str], minutes: int, period: int) -> Optional[float]:
    query = load_metric_window(
        metric_name=metric_name,
        namespace=namespace,
        minutes=minutes,
        period=period,
        stat="Average",
        dimensions=dimensions,
    )
    response = client.get_metric_statistics(
        Namespace=query.namespace,
        MetricName=query.metric_name,
        Dimensions=query.to_cloudwatch_dimensions(),
        StartTime=query.start_time,
        EndTime=query.end_time,
        Period=query.period,
        Statistics=["Average"],
    )
    datapoints = response.get("Datapoints", [])
    values = [float(point["Average"]) for point in datapoints if "Average" in point]
    if not values:
        return None
    return sum(values) / len(values)


def compare_metric_series(
    metric_name: str,
    namespace: str,
    left_dimensions: Dict[str, str],
    right_dimensions: Dict[str, str],
    minutes: int = 15,
    period: int = 60,
    region_name: Optional[str] = None,
) -> MetricComparison:
    client = get_cloudwatch_client(region_name=region_name)
    left_average = _query_average(client, metric_name, namespace, left_dimensions, minutes, period)
    right_average = _query_average(client, metric_name, namespace, right_dimensions, minutes, period)
    delta = None if left_average is None or right_average is None else left_average - right_average
    ratio = None if left_average is None or right_average in (None, 0) else left_average / right_average
    return MetricComparison(
        metric_name=metric_name,
        namespace=namespace,
        left_filter=dict(left_dimensions),
        right_filter=dict(right_dimensions),
        left_average=left_average,
        right_average=right_average,
        delta=delta,
        ratio=ratio,
    )
