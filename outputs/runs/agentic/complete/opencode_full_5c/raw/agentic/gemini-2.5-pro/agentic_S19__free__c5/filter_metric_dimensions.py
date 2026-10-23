import os
from datetime import datetime, timedelta
from google.cloud.monitoring_v3.types import TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client
from observability_models import MetricData, TimeSeriesPoint


def query_metric_with_filter(
    project_id: str, metric_name: str, dimension_filter: str, minutes_ago: int = 60
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

    full_filter = f'metric.type = "{metric_name}" AND {dimension_filter}'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": full_filter,
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

    instance_name = os.environ.get(
        "GCE_INSTANCE_NAME"
    )  # e.g. 'gke-cluster-1-default-pool-...'
    if not instance_name:
        raise ValueError(
            "GCE_INSTANCE_NAME environment variable must be set for the filter"
        )

    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    # Example: resource.labels.instance_name = "your-instance-name"
    d_filter = f'resource.labels.instance_name = "{instance_name}"'

    data = query_metric_with_filter(project, metric_type, d_filter, minutes_ago=15)
    for series in data:
        print(f"Filtered query for {instance_name}:")
        print(f"Metric: {series.metric_name}")
        print(f"Resource: {series.resource_labels}")
        for point in series.points:
            print(f"  {point.timestamp}: {point.value}")
