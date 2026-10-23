import time
from datetime import datetime, timedelta, timezone
from google.cloud.monitoring_v3.services.metric_service import MetricServiceClient
from observability_client import get_monitoring_client
from observability_models import MetricTimeSeries, TimeSeriesDataPoint


def query_metrics_by_dimension(
    project_id: str, metric_type: str, window_minutes: int, dimension_filter: dict
) -> list[MetricTimeSeries]:
    client: MetricServiceClient = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    filter_str = f'metric.type = "{metric_type}"'
    for key, value in dimension_filter.items():
        filter_str += f' AND resource.labels.{key} = "{value}"'

    request = {
        "name": project_name,
        "filter": filter_str,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results = client.list_time_series(request)

    output_series = []
    for result in results:
        points = []
        for point in result.points:
            points.append(
                TimeSeriesDataPoint(
                    timestamp=point.interval.end_time.rfc3339(),
                    value=point.value.double_value,
                )
            )

        series = MetricTimeSeries(
            metric_name=result.metric.type,
            resource_labels=dict(result.resource.labels),
            points=points,
        )
        output_series.append(series)

    return output_series
