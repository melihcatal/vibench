from typing import Dict, Optional

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, parse_time_window, project_name_from_env
from observability_models import ComparisonResult, MetricQueryRequest, normalize_points, summarize_series


def compare_metric_series(metric_name: str, left_dimensions: Optional[Dict[str, str]] = None, right_dimensions: Optional[Dict[str, str]] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, minutes: int = 60) -> ComparisonResult:
    client = get_monitoring_client()
    project_name = project_name_from_env()
    window = parse_time_window(start_time=start_time, end_time=end_time, minutes=minutes)
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": window.start_time,
            "end_time": window.end_time,
        }
    )

    def build_filter(dimensions: Optional[Dict[str, str]]) -> str:
        clauses = [f'metric.type = "{metric_name}"']
        for key, value in (dimensions or {}).items():
            clauses.append(f'metric.labels."{key}" = "{value}"')
        return " AND ".join(clauses)

    def fetch(dimensions: Optional[Dict[str, str]]):
        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=build_filter(dimensions),
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )
        points = []
        for ts in client.list_time_series(request=request):
            points.extend(normalize_points(ts.points))
        return summarize_series(points)

    left = fetch(left_dimensions)
    right = fetch(right_dimensions)
    return ComparisonResult(
        request=MetricQueryRequest(metric_name=metric_name, start_time=window.start_time, end_time=window.end_time, dimensions={"left": left_dimensions or {}, "right": right_dimensions or {}}),
        left=left,
        right=right,
        difference=left.get("mean", 0.0) - right.get("mean", 0.0),
    )
