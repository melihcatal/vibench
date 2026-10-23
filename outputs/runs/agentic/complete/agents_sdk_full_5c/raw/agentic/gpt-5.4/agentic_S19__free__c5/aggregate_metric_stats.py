from __future__ import annotations

from typing import Any, Dict

from query_metric_window import query_metric_window
from observability_models import MetricPoint, compute_aggregate_stats


def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    minutes: int = 60,
    alignment_period_seconds: int = 300,
    per_series_aligner: str = "ALIGN_MEAN",
) -> Dict[str, Any]:
    payload = query_metric_window(
        project_id=project_id,
        metric_type=metric_type,
        minutes=minutes,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
    )
    points = [MetricPoint(**point) for point in payload["points"]]
    stats = compute_aggregate_stats(metric_type, points)
    return stats.__dict__
