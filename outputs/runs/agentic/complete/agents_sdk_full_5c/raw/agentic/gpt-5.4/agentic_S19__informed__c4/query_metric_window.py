from __future__ import annotations

from typing import Any, Dict, List

from google.cloud import monitoring_v3

from observability_client import build_aggregation, build_metric_filter, get_metric_client, get_project_id, project_name, time_interval_for_minutes
from observability_models import MetricWindowRequest, normalize_time_series, series_to_dict


GOOGLE_CLOUD_MONITORING_API = "monitoring.googleapis.com"


def query_metric_window(request: MetricWindowRequest) -> Dict[str, Any]:
    client = get_metric_client()
    pager = client.list_time_series(
        request={
            "name": project_name(get_project_id(request.project_id)),
            "filter": build_metric_filter(request),
            "interval": time_interval_for_minutes(request.minutes),
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView[request.view],
            "aggregation": build_aggregation(request),
        }
    )
    series: List[Dict[str, Any]] = [series_to_dict(normalize_time_series(item)) for item in pager]
    return {"provider": "Google Cloud Monitoring", "series": series}
