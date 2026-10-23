from __future__ import annotations

from typing import Any, Dict, List

from google.cloud import monitoring_v3

from observability_client import build_metric_filter, get_metric_client, get_project_id, project_name, time_interval_for_minutes
from observability_models import AggregatedMetricResponse, MetricPoint, MetricWindowRequest, normalize_time_series


GCP_MONITORING_ALIGNER = "ALIGN_MEAN"
GCP_MONITORING_REDUCER = "REDUCE_MEAN"


def aggregate_metric_stats(request: MetricWindowRequest) -> Dict[str, Any]:
    client = get_metric_client()
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": request.alignment_period_seconds},
        per_series_aligner=GCP_MONITORING_ALIGNER,
        cross_series_reducer=request.cross_series_reducer or GCP_MONITORING_REDUCER,
        group_by_fields=request.group_by_fields,
    )
    pager = client.list_time_series(
        request={
            "name": project_name(get_project_id(request.project_id)),
            "filter": build_metric_filter(request),
            "interval": time_interval_for_minutes(request.minutes),
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    all_points: List[MetricPoint] = []
    count = 0
    for item in pager:
        normalized = normalize_time_series(item)
        all_points.extend(normalized.points)
        count += 1
    response = AggregatedMetricResponse(metric_type=request.metric_type, series_count=count, points=all_points)
    return {"provider": "Google Cloud Monitoring", "metric_type": response.metric_type, "series_count": response.series_count, "points": [p.__dict__ for p in response.points]}
