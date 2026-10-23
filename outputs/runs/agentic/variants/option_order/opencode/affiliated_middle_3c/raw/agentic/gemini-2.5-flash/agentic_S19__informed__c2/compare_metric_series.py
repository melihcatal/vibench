import datetime
from google.cloud import monitoring_v3
from observability_client import get_metric_service_client, get_project_id


def compare_metric_series(
    metric_type: str, filter_a: str, filter_b: str, minutes_ago: int = 60
):
    """
    Compares metric values for two different filters over the same time window.
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

    # Query for the first series
    response_a = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}" AND {filter_a}',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    # Query for the second series
    response_b = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}" AND {filter_b}',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    series_a_data = []
    for series in response_a.time_series:
        for point in series.points:
            series_a_data.append(
                {
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                    "timestamp": point.interval.end_time.timestamp(),
                    "resource_labels": dict(series.resource.labels),
                }
            )

    series_b_data = []
    for series in response_b.time_series:
        for point in series.points:
            series_b_data.append(
                {
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                    "timestamp": point.interval.end_time.timestamp(),
                    "resource_labels": dict(series.resource.labels),
                }
            )

    return {"series_a": series_a_data, "series_b": series_b_data}
