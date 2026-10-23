from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from google.cloud import monitoring_v3

from observability_client import load_config, monitored_project_name, monitoring_client
from observability_models import MetricSeriesPoint, MetricSeriesResponse, MetricWindowRequest, normalize_point


def query_metric_window(request: MetricWindowRequest) -> MetricSeriesResponse:
    cfg = load_config()
    client = monitoring_client()
    project_name = monitored_project_name(cfg.project_id)
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": request.start_time,
            "end_time": request.end_time,
        }
    )
    flt = request.filter_expression or f'metric.type = "{request.metric_type}"'
    if request.resource_labels:
        for key, value in request.resource_labels.items():
            flt += f' AND resource.labels."{key}" = "{value}"'

    results: List[MetricSeriesPoint] = []
    for time_series in client.list_time_series(
        request={
            "name": project_name,
            "filter": flt,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    ):
        for point in time_series.points:
            ts = point.interval.end_time or point.interval.start_time
            val = point.value.double_value or point.value.int64_value or point.value.distribution_value.count
            labels: Dict[str, str] = dict(time_series.resource.labels)
            results.append(normalize_point(ts, float(val), labels))

    return MetricSeriesResponse(
        metric_type=request.metric_type,
        points=results,
        summary={"project": project_name, "series_count": len(results)},
    )
