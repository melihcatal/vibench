from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client
from observability_models import MetricAggregationRequest


def aggregate_metric_stats(request: MetricAggregationRequest) -> Dict[str, Any]:
    config = load_config()
    client = metric_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=request.minutes)
    interval = monitoring_v3.TimeInterval({"end_time": end_time, "start_time": start_time})

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": max(60, request.minutes * 60 // 10)},
            "per_series_aligner": getattr(monitoring_v3.Aggregation.Aligner, request.aligner),
            "cross_series_reducer": getattr(monitoring_v3.Aggregation.Reducer, request.reducer),
            "group_by_fields": list(request.group_by_fields),
        }
    )

    series = client.list_time_series(
        request={
            "name": f"projects/{config.project_id}",
            "filter": request.filter_expression or f'metric.type = "{request.metric_type}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    totals = []
    for ts in series:
        for point in ts.points:
            val = point.value.double_value or point.value.int64_value or point.value.distribution_value.count
            totals.append(float(val))

    return {
        "metric_type": request.metric_type,
        "count": len(totals),
        "mean": sum(totals) / len(totals) if totals else None,
        "min": min(totals) if totals else None,
        "max": max(totals) if totals else None,
        "project_id": config.project_id,
    }
