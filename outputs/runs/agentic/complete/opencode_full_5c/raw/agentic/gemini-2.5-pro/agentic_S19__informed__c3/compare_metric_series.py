from datetime import datetime, timedelta, timezone
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricTimeSeries, TimeSeriesDataPoint


def compare_metric_data(
    project_id: str,
    metric_type: str,
    window_minutes: int,
    filter1: dict,
    filter2: dict,
) -> dict[str, MetricTimeSeries | None]:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=window_minutes)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    def _get_series(metric_filter: dict):
        filter_str = f'metric.type = "{metric_type}"'
        for key, value in metric_filter.items():
            filter_str += f' AND resource.labels.{key} = "{value}"'

        request = {
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
        results = client.list_time_series(request)

        # Assuming one series per filter for comparison
        for result in results:
            points = [
                TimeSeriesDataPoint(
                    timestamp=p.interval.end_time.rfc3339(), value=p.value.double_value
                )
                for p in result.points
            ]
            return MetricTimeSeries(
                metric_name=result.metric.type,
                resource_labels=dict(result.resource.labels),
                points=points,
            )
        return None

    series1 = _get_series(filter1)
    series2 = _get_series(filter2)

    return {"series1": series1, "series2": series2}
