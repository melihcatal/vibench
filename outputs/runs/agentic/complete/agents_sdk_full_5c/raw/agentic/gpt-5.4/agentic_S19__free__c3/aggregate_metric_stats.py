from __future__ import annotations

from statistics import mean
from typing import Optional

from observability_client import monitoring_client
from observability_models import MetricStatsResponse, MetricWindowRequest, normalize_time_series_points


_STAT_ALGINERS = {
    "mean": "ALIGN_MEAN",
    "max": "ALIGN_MAX",
    "min": "ALIGN_MIN",
    "sum": "ALIGN_SUM",
}


def aggregate_metric_stats(
    metric_type: str,
    statistic: str = "mean",
    minutes: int = 60,
    project_id: Optional[str] = None,
    filter_text: Optional[str] = None,
) -> MetricStatsResponse:
    aligner = _STAT_ALGINERS.get(statistic.lower())
    if not aligner:
        raise ValueError("statistic must be one of: mean, max, min, sum")
    client = monitoring_client(project_id)
    request = MetricWindowRequest(
        project_id=client.project_id,
        metric_type=metric_type,
        minutes=minutes,
        alignment_period_seconds=max(minutes * 60, 60),
        per_series_aligner=aligner,
        filter_text=filter_text,
    )
    payload = client.list_time_series(request=request, view="FULL")
    points = normalize_time_series_points(payload.get("timeSeries", []))
    values = [p.value for p in points]
    if not values:
        value = None
    elif statistic.lower() == "mean":
        value = mean(values)
    elif statistic.lower() == "max":
        value = max(values)
    elif statistic.lower() == "min":
        value = min(values)
    else:
        value = sum(values)
    return MetricStatsResponse(metric_type=metric_type, statistic=statistic.lower(), value=value, samples=len(values))
