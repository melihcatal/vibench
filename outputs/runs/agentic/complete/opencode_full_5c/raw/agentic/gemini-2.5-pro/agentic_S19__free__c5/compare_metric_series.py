import os
from datetime import datetime, timedelta
from typing import Dict, List

from google.cloud.monitoring_v3.types import TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client
from observability_models import MetricData, TimeSeriesPoint


def get_series(client, project_name, metric_filter, interval) -> List[MetricData]:
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": metric_filter,
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


def compare_two_metric_series(
    project_id: str,
    metric_name: str,
    filter1: str,
    filter2: str,
    minutes_ago: int = 60,
) -> Dict[str, List[MetricData]]:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)

    start_timestamp = Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = Timestamp()
    end_timestamp.FromDatetime(now)

    interval = TimeInterval(start_time=start_timestamp, end_time=end_timestamp)

    metric_filter1 = f'metric.type = "{metric_name}" AND {filter1}'
    metric_filter2 = f'metric.type = "{metric_name}" AND {filter2}'

    series1 = get_series(client, project_name, metric_filter1, interval)
    series2 = get_series(client, project_name, metric_filter2, interval)

    return {"series1": series1, "series2": series2}


if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    instance1 = os.environ.get("GCE_INSTANCE_1")
    instance2 = os.environ.get("GCE_INSTANCE_2")

    if not all([instance1, instance2]):
        raise ValueError(
            "GCE_INSTANCE_1 and GCE_INSTANCE_2 environment variables are required."
        )

    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    filter_1 = f'resource.labels.instance_name = "{instance1}"'
    filter_2 = f'resource.labels.instance_name = "{instance2}"'

    comparison = compare_two_metric_series(
        project, metric_type, filter_1, filter_2, minutes_ago=15
    )

    print(f"Comparison for instances '{instance1}' and '{instance2}'")
    for key, series_list in comparison.items():
        print(f"\n--- {key} ---")
        for series in series_list:
            print(f"  Resource: {series.resource_labels}")
            for point in series.points[-5:]:  # Last 5 points
                print(f"    {point.timestamp}: {point.value:.4f}")
