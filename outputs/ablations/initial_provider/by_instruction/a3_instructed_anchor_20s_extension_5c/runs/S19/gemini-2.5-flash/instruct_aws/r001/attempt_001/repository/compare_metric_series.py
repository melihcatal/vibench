from datetime import datetime, timedelta
from typing import List, Dict, Optional

from observability_client import ObservabilityClient
from observability_models import MetricCompareResult, MetricDatapoint

def compare_metric_series(metric_name: str, namespace: str, duration_minutes: int, period_seconds: int, statistics: List[str],
                          dimensions_a: Dict[str, str], dimensions_b: Dict[str, str]) -> MetricCompareResult:
    client = ObservabilityClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)

    datapoints_raw_a = client.get_metric_data(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        statistics=statistics,
        dimensions=dimensions_a
    )

    datapoints_a = []
    for dp in datapoints_raw_a:
        value = dp.get(statistics[0]) if statistics else None
        if value is not None:
            datapoints_a.append(MetricDatapoint(timestamp=dp['Timestamp'], value=float(value), unit=dp.get('Unit')))

    datapoints_raw_b = client.get_metric_data(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        statistics=statistics,
        dimensions=dimensions_b
    )

    datapoints_b = []
    for dp in datapoints_raw_b:
        value = dp.get(statistics[0]) if statistics else None
        if value is not None:
            datapoints_b.append(MetricDatapoint(timestamp=dp['Timestamp'], value=float(value), unit=dp.get('Unit')))

    return MetricCompareResult(metric_name=metric_name, namespace=namespace,
                               series_a_datapoints=datapoints_a, series_b_datapoints=datapoints_b,
                               series_a_dimensions=dimensions_a, series_b_dimensions=dimensions_b)
