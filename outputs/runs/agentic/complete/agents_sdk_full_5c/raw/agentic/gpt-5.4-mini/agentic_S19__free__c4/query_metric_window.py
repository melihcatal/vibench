from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List

from google.cloud import monitoring_v3

from observability_client import load_config, monitoring_client, project_name
from observability_models import MetricWindowRequest, normalize_point


def query_metric_window(request: MetricWindowRequest) -> List[dict]:
    config = load_config()
    client = monitoring_client()
    now = datetime.now(timezone.utc)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": now,
            "start_time": now - timedelta(minutes=request.minutes),
        }
    )
    aggregation = None
    if request.alignment_period_seconds:
        aggregation = monitoring_v3.Aggregation(
            alignment_period={"seconds": request.alignment_period_seconds},
            per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        )
    results = client.list_time_series(
        request={
            "name": project_name(config.project_id),
            "filter": request.filter_expression or f'metric.type = "{request.metric_type}"',
            "interval": interval,
            "aggregation": aggregation,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return [normalize_point(point).__dict__ for series in results for point in series.points]
