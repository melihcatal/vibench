import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, parse_time_window, project_name_from_env
from observability_models import MetricQueryRequest, MetricWindowResult, normalize_points


def query_metric_window(metric_name: str, start_time: Optional[str] = None, end_time: Optional[str] = None, minutes: int = 60, alignment_period_seconds: int = 60, per_series_aligner: str = "ALIGN_MEAN") -> MetricWindowResult:
    client = get_monitoring_client()
    project_name = project_name_from_env()
    window = parse_time_window(start_time=start_time, end_time=end_time, minutes=minutes)
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": window.start_time,
            "end_time": window.end_time,
        }
    )
    aligner = getattr(monitoring_v3.Aggregation.Aligner, per_series_aligner, monitoring_v3.Aggregation.Aligner.ALIGN_MEAN)
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": alignment_period_seconds},
            "per_series_aligner": aligner,
        }
    )
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=f'metric.type = "{metric_name}"',
        interval=interval,
        aggregation=aggregation,
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
    return MetricWindowResult(request=MetricQueryRequest(metric_name=metric_name, start_time=window.start_time, end_time=window.end_time, dimensions={}), series=series)
