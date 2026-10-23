from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Any

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client
from observability_models import MetricWindowRequest, MetricSeries, normalize_points, summarize_series


def query_metric_window(request: MetricWindowRequest) -> Dict[str, Any]:
    config = load_config()
    client = metric_client()
    project_name = f"projects/{config.project_id}"
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=request.minutes)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": end_time,
            "start_time": start_time,
        }
    )

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": max(60, request.minutes * 60 // 10)},
            "per_series_aligner": getattr(monitoring_v3.Aggregation.Aligner, request.aligner),
        }
    )

    filt = request.filter_expression or f'metric.type = "{request.metric_type}"'
    series = client.list_time_series(
        request={
            "name": project_name,
            "filter": filt,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    points = []
    for ts in series:
        for point in ts.points:
            timestamp = point.interval.end_time.ToDatetime().replace(tzinfo=timezone.utc)
            value = point.value.double_value or point.value.int64_value or point.value.distribution_value.count
            points.append(type("Point", (), {"timestamp": timestamp, "value": float(value), "labels": dict(ts.resource.labels)}))

    metric_series = MetricSeries(metric_type=request.metric_type, points=normalize_points(points), metadata={"resource_type": request.resource_type})
    return summarize_series(metric_series)
