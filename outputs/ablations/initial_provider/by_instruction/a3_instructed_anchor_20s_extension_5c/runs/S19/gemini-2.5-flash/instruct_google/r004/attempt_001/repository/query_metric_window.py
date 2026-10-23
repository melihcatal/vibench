from google.cloud import monitoring_v3
import os
from datetime import datetime, timedelta

def query_metric_window(project_id: str, metric_type: str, minutes_ago: int = 60):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    end_time = now
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    query = f"fetch gce_instance | metric {metric_type} | within {minutes_ago}m"

    results = client.query_time_series(
        name=project_name,
        query=query,
        interval=interval,
    )

    time_series_data = []
    for time_series in results:
        for point in time_series.points:
            time_series_data.append({
                "metric": time_series.metric.type,
                "value": point.value.double_value,
                "timestamp": point.interval.end_time.timestamp(),
                "resource": {
                    "type": time_series.resource.type,
                    "labels": dict(time_series.resource.labels)
                }
            })
    return time_series_data
