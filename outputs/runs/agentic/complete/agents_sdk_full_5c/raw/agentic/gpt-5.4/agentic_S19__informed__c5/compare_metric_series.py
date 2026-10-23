from __future__ import annotations

from typing import Dict, List

from observability_client import build_aggregation, build_filter, build_time_interval, get_metric_client, load_config, project_name
from observability_models import MetricPoint, build_metric_point, summarize_points



def _fetch_points(client, project: str, metric_type: str, minutes: int, resource_type: str | None, resource_labels: dict | None, alignment_period_seconds: int) -> List[MetricPoint]:
    request = {
        "name": project_name(project),
        "filter": build_filter(metric_type=metric_type, resource_type=resource_type, resource_labels=resource_labels),
        "interval": build_time_interval(minutes),
        "view": "FULL",
        "aggregation": build_aggregation(alignment_period_seconds=alignment_period_seconds, per_series_aligner="ALIGN_MEAN"),
    }
    points: List[MetricPoint] = []
    for series in client.list_time_series(request=request):
        rlabels = dict(getattr(series.resource, "labels", {}) or {})
        mlabels = dict(getattr(series.metric, "labels", {}) or {})
        for point in series.points:
            normalized = build_metric_point(point, resource_labels=rlabels, metric_labels=mlabels)
            if normalized:
                points.append(normalized)
    return points



def compare_metric_series(metric_type: str, left_resource_labels: dict, right_resource_labels: dict, minutes: int = 15, project_id: str | None = None, resource_type: str | None = None, alignment_period_seconds: int = 60) -> Dict[str, object]:
    config = load_config(project_id)
    client = get_metric_client()
    left_points = _fetch_points(client, config.project_id, metric_type, minutes, resource_type, left_resource_labels, alignment_period_seconds)
    right_points = _fetch_points(client, config.project_id, metric_type, minutes, resource_type, right_resource_labels, alignment_period_seconds)
    left_stats = summarize_points(metric_type, left_points)
    right_stats = summarize_points(metric_type, right_points)
    average_delta = None
    if left_stats.average is not None and right_stats.average is not None:
        average_delta = left_stats.average - right_stats.average
    return {
        "provider": "Google Cloud Monitoring",
        "project_id": config.project_id,
        "metric_type": metric_type,
        "left": {"resource_labels": left_resource_labels, "statistics": left_stats.__dict__},
        "right": {"resource_labels": right_resource_labels, "statistics": right_stats.__dict__},
        "average_delta": average_delta,
    }
