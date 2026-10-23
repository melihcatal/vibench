import os
from datetime import datetime, timedelta

from google.cloud import monitoring_v3
from google.api import metric_pb2

def query_metric_window(project_id: str, metric_type: str, resource_type: str, minutes_ago: int = 60, interval_seconds: int = 60) -> list:
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())},
    )

    query = f"fetch {resource_type}::\"{metric_type}\""

    response = client.list_time_series(
        name=project_name,
        filter=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = []
    for series in response:
        for point in series.points:
            results.append({
                "timestamp": point.interval.end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "value": point.value.double_value if point.value.value_type == metric_pb2.MetricDescriptor.ValueType.DOUBLE else point.value.int64_value,
                "metric_type": series.metric.type,
                "resource_labels": {k: v for k, v in series.resource.labels.items()}
            })
    return results