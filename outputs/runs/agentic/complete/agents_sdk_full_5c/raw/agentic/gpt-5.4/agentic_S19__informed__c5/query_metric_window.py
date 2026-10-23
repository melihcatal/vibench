from __future__ import annotations

from typing import Dict, List

from observability_client import build_aggregation, build_filter, build_time_interval, get_metric_client, load_config, project_name
from observability_models import MetricPoint, MetricSeries, build_metric_point



def query_metric_window(metric_type: str, minutes: int = 15, project_id: str | None = None, resource_type: str | None = None, alignment_period_seconds: int = 60) -> Dict[str, object]:
    config = load_config(project_id)
    client = get_metric_client()
    request = {
        "name": project_name(config.project_id),
        "filter": build_filter(metric_type=metric_type, resource_type=resource_type),
        "interval": build_time_interval(minutes),
        "view": "FULL",
        "aggregation": build_aggregation(alignment_period_seconds=alignment_period_seconds, per_series_aligner="ALIGN_MEAN"),
    }
    results = client.list_time_series(request=request)
    series_list: List[Dict[str, object]] = []
    for series in results:
        resource_labels = dict(getattr(series.resource, "labels", {}) or {})
        metric_labels = dict(getattr(series.metric, "labels", {}) or {})
        points: List[MetricPoint] = []
        for point in series.points:
            normalized = build_metric_point(point, resource_labels=resource_labels, metric_labels=metric_labels)
            if normalized:
                points.append(normalized)
        series_list.append(
            MetricSeries(
                metric_type=series.metric.type,
                unit=getattr(series, "unit", None),
                points=points,
            ).__dict__
        )
    return {
        "provider": "Google Cloud Monitoring",
        "project_id": config.project_id,
        "metric_type": metric_type,
        "series": series_list,
    }
