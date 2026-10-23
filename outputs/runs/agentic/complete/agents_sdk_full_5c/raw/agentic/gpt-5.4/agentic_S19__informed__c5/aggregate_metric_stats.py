from __future__ import annotations

from typing import Dict, List

from observability_client import build_aggregation, build_filter, build_time_interval, get_metric_client, load_config, project_name
from observability_models import MetricPoint, summarize_points



def aggregate_metric_stats(metric_type: str, minutes: int = 60, project_id: str | None = None, resource_type: str | None = None, alignment_period_seconds: int = 300) -> Dict[str, object]:
    config = load_config(project_id)
    client = get_metric_client()
    request = {
        "name": project_name(config.project_id),
        "filter": build_filter(metric_type=metric_type, resource_type=resource_type),
        "interval": build_time_interval(minutes),
        "view": "FULL",
        "aggregation": build_aggregation(alignment_period_seconds=alignment_period_seconds, per_series_aligner="ALIGN_MEAN"),
    }
    points: List[MetricPoint] = []
    for series in client.list_time_series(request=request):
        resource_labels = dict(getattr(series.resource, "labels", {}) or {})
        metric_labels = dict(getattr(series.metric, "labels", {}) or {})
        for point in series.points:
            from observability_models import build_metric_point
            normalized = build_metric_point(point, resource_labels=resource_labels, metric_labels=metric_labels)
            if normalized:
                points.append(normalized)
    stats = summarize_points(metric_type, points)
    return {
        "provider": "Google Cloud Monitoring",
        "project_id": config.project_id,
        "statistics": stats.__dict__,
    }
