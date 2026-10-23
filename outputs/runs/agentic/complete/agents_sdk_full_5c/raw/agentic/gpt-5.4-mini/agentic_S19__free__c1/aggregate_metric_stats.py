from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client, project_name, parse_filters
from observability_models import AggregatedMetricStatsRequest, normalize_time_series


def aggregate_metric_stats(metric_type: str, minutes: int, resource_labels: Dict[str, str] | None = None, reduction: str = "mean") -> Dict[str, Any]:
    config = load_config()
    client = metric_client()
    now = datetime.now(timezone.utc)
    request = AggregatedMetricStatsRequest(metric_type=metric_type, minutes=minutes, reduction=reduction, resource_labels=resource_labels or {})
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": now - timedelta(minutes=request.minutes),
            "end_time": now,
        }
    )
    aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    if request.reduction == "max":
        aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MAX
    elif request.reduction == "min":
        aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MIN
    response = client.list_time_series(
        request={
            "name": project_name(config),
            "filter": " AND ".join([f'metric.type = "{request.metric_type}"'] + ([parse_filters(request.resource_labels)] if request.resource_labels else [])),
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": {
                "alignment_period": {"seconds": 60},
                "per_series_aligner": aligner,
                "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
            },
        }
    )
    normalized = normalize_time_series(response)
    values = normalized.values
    return {
        "metric_type": normalized.metric_type,
        "count": len(values),
        "mean": sum(values) / len(values) if values else 0.0,
        "min": min(values) if values else 0.0,
        "max": max(values) if values else 0.0,
    }
