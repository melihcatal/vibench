import os
from datetime import datetime, timedelta
from google.cloud.monitoring_v3.types import TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client
from observability_models import MetricData, TimeSeriesPoint


def query_metric(
    project_id: str, metric_name: str, minutes_ago: int = 60
) -> list[MetricData]:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)

    start_timestamp = Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = Timestamp()
    end_timestamp.FromDatetime(now)

    interval = TimeInterval(start_time=start_timestamp, end_time=end_timestamp)

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_name}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    output = []
    for result in results:
        points = [
            TimeSeriesPoint(
                timestamp=p.interval.end_time.isoformat(), value=p.value.double_value
            )
            for p in result.points
        ]
        output.append(
            MetricData(
                metric_name=result.metric.type,
                resource_labels=dict(result.resource.labels),
                points=points,
            )
        )
    return output


if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    # Example: Query CPU utilization for the last 10 minutes
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    data = query_metric(project, metric_type, minutes_ago=10)
    for series in data:
        print(f"Metric: {series.metric_name}")
        print(f"Resource: {series.resource_labels}")
        for point in series.points:
            print(f"  {point.timestamp}: {point.value}")
