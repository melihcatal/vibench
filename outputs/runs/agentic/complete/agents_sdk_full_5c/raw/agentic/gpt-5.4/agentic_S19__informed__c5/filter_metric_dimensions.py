from __future__ import annotations

from typing import Dict, List

from observability_client import build_aggregation, build_filter, build_time_interval, get_metric_client, load_config, project_name
from observability_models import MetricSeries, build_metric_point



def filter_metric_dimensions(metric_type: str, minutes: int = 15, project_id: str | None = None, resource_type: str | None = None, resource_labels: dict | None = None, metric_labels: dict | None = None, alignment_period_seconds: int = 60) -> Dict[str, object]:
    config = load_config(project_id)
    client = get_metric_client()
    request = {
        "name": project_name(config.project_id),
        "filter": build_filter(metric_type=metric_type, resource_type=resource_type, resource_labels=resource_labels, metric_labels=metric_labels),
        "interval": build_time_interval(minutes),
        "view": "FULL",
        "aggregation": build_aggregation(alignment_period_seconds=alignment_period_seconds, per_series_aligner="ALIGN_MEAN"),
    }
    filtered: List[Dict[str, object]] = []
    for series in client.list_time_series(request=request):
        rlabels = dict(getattr(series.resource, "labels", {}) or {})
        mlabels = dict(getattr(series.metric, "labels", {}) or {})
        points = [p for p in (build_metric_point(point, resource_labels=rlabels, metric_labels=mlabels) for point in series.points) if p]
        filtered.append(MetricSeries(metric_type=series.metric.type, unit=getattr(series, "unit", None), points=points).__dict__)
    return {
        "provider": "Google Cloud Monitoring",
        "project_id": config.project_id,
        "applied_filter": request["filter"],
        "series": filtered,
    }
