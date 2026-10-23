import datetime
from google.cloud import monitoring_v3
from observability_client import get_metric_service_client, get_project_id


def query_metric_window(metric_type: str, minutes_ago: int = 60):
    """
    Queries recent datapoints for a named metric over a specified time window.
    """
    client = get_metric_service_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"

    now = datetime.datetime.now(datetime.timezone.utc)
    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(now.timestamp())},
        start_time={
            "seconds": int((now - datetime.timedelta(minutes=minutes_ago)).timestamp())
        },
    )

    query_filter = f'metric.type = "{metric_type}"'

    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    results = []
    for series in response.time_series:
        for point in series.points:
            results.append(
                {
                    "metric": series.metric.type,
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                    "timestamp": point.interval.end_time.timestamp(),
                    "resource_labels": dict(series.resource.labels),
                }
            )
    return results
