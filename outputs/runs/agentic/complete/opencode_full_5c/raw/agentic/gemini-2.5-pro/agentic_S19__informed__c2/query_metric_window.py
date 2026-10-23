import time
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from observability_client import get_gcp_observability_client, get_gcp_project_name
from observability_models import QueryWindowRequest, MetricTimeSeries, TimeSeriesPoint


def query_metric_window(request: QueryWindowRequest) -> list[MetricTimeSeries]:
    client = get_gcp_observability_client(request.project_id)
    if not client:
        return []

    project_name = get_gcp_project_name(request.project_id)
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {
                "seconds": seconds - (request.minutes_ago * 60),
                "nanos": nanos,
            },
        }
    )

    filter_str = f'metric.type = "{request.metric_name}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    time_series_data = []
    for result in results:
        points = []
        for point in result.points:
            points.append(
                TimeSeriesPoint(
                    timestamp=point.interval.end_time.rfc3339(),
                    value=point.value.double_value,
                )
            )

        dimensions = {
            label: result.metric.labels[label] for label in result.metric.labels
        }

        time_series_data.append(
            MetricTimeSeries(
                metric_name=result.metric.type, dimensions=dimensions, points=points
            )
        )
    return time_series_data
