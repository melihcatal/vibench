from typing import Dict, Optional

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, parse_time_window, project_name_from_env
from observability_models import MetricQueryRequest, MetricWindowResult, normalize_points


def filter_metric_dimensions(metric_name: str, dimensions: Optional[Dict[str, str]] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, minutes: int = 60) -> MetricWindowResult:
    client = get_monitoring_client()
    project_name = project_name_from_env()
    window = parse_time_window(start_time=start_time, end_time=end_time, minutes=minutes)
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": window.start_time,
            "end_time": window.end_time,
        }
    )
    clauses = [f'metric.type = "{metric_name}"']
    for key, value in (dimensions or {}).items():
        clauses.append(f'metric.labels."{key}" = "{value}"')
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=" AND ".join(clauses),
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    series = []
    for ts in client.list_time_series(request=request):
        series.append(
            {
                "metric": dict(ts.metric),
                "resource": dict(ts.resource),
                "points": normalize_points(ts.points),
            }
        )
    return MetricWindowResult(request=MetricQueryRequest(metric_name=metric_name, start_time=window.start_time, end_time=window.end_time, dimensions=dimensions or {}), series=series)
