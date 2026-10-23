from typing import Dict, Optional

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, parse_time_window, project_name_from_env
from observability_models import MetricQueryRequest, summarize_series, normalize_points


def metric_summary(metric_name: str, start_time: Optional[str] = None, end_time: Optional[str] = None, minutes: int = 60) -> Dict[str, float]:
    client = get_monitoring_client()
    project_name = project_name_from_env()
    window = parse_time_window(start_time=start_time, end_time=end_time, minutes=minutes)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=f'metric.type = "{metric_name}"',
        interval=monitoring_v3.TimeInterval({"start_time": window.start_time, "end_time": window.end_time}),
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    points = []
    for ts in client.list_time_series(request=request):
        points.extend(normalize_points(ts.points))
    summary = summarize_series(points)
    summary["window_minutes"] = float(minutes)
    return summary
