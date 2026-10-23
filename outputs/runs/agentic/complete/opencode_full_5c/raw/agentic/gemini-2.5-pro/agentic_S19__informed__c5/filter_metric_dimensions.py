from datetime import datetime, timedelta, timezone
from typing import Dict
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricTimeSeries, MetricDataPoint
from google.cloud import monitoring_v3


def query_metric_with_dimension_filter(
    project_id: str,
    metric_type: str,
    minutes_ago: int,
    dimension_filters: Dict[str, str],
) -> list[MetricTimeSeries]:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(now.timestamp())},
        }
    )

    filter_str = f'metric.type = "{metric_type}"'
    for key, value in dimension_filters.items():
        filter_str += f' AND {key} = "{value}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    time_series_list = []
    for result in results:
        points = [
            MetricDataPoint(
                timestamp=p.interval.end_time.rfc3339(), value=p.value.double_value
            )
            for p in result.points
        ]
        ts = MetricTimeSeries(
            metric_kind=str(result.metric_kind),
            value_type=str(result.value_type),
            metric_labels=dict(result.metric.labels),
            resource_labels=dict(result.resource.labels),
            points=points,
        )
        time_series_list.append(ts)

    return time_series_list


if __name__ == "__main__":
    project = get_project_id()
    metric = "compute.googleapis.com/instance/cpu/utilization"
    # Filter for a specific GCE instance zone
    filters = {"resource.label.zone": "us-central1-a"}
    series = query_metric_with_dimension_filter(project, metric, 60, filters)
    for ts in series:
        print(ts)
