from google.cloud import monitoring_v3
from datetime import datetime, timedelta
from typing import Dict, List
from observability_client import ObservabilityClient
from observability_models import MetricPoint, MetricSeries, normalize_labels


def filter_metric_dimensions(
    metric_name: str, dimensions: Dict[str, str], hours: int = 1
) -> MetricSeries:
    client = ObservabilityClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

    filter_parts = [f"resource.label.{k}='{v}'" for k, v in dimensions.items()]
    filter_str = " AND ".join(filter_parts)

    series = client.list_time_series(
        f"custom.googleapis.com/{metric_name}", interval, filter_str
    )
    points = []

    for ts in series:
        for point in ts.points:
            points.append(
                MetricPoint(
                    value=float(point.value.double_value),
                    timestamp=point.interval.end_time.ToDatetime(),
                    labels=normalize_labels(dict(ts.resource.labels)),
                )
            )

    return MetricSeries(metric_type=metric_name, points=points)
