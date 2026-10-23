from __future__ import annotations

from typing import Any, Dict

from query_metric_window import query_metric_window
from observability_models import MetricPoint, summarize_trend


def metric_summary(
    project_id: str,
    metric_type: str,
    minutes: int = 30,
    alignment_period_seconds: int = 300,
) -> Dict[str, Any]:
    payload = query_metric_window(
        project_id=project_id,
        metric_type=metric_type,
        minutes=minutes,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner="ALIGN_MEAN",
    )
    summary = summarize_trend(metric_type, [MetricPoint(**point) for point in payload["points"]])
    return summary.__dict__
