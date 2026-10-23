from datetime import datetime, timedelta, timezone
from google.cloud.monitoring_v3.services.metric_service import pagers
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricTimeSeries, MetricDataPoint


def query_metric_window(
    project_id: str, metric_type: str, minutes_ago: int
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

    results: pagers.ListTimeSeriesPager = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}"',
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
    # Example: GCE CPU utilization
    metric = "compute.googleapis.com/instance/cpu/utilization"
    series = query_metric_window(project, metric, 60)
    for ts in series:
        print(ts)
