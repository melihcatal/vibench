import json

from google.cloud import monitoring_v3

from observability_client import load_observability_config, monitoring_client, project_name
from observability_models import compare_series


def _build_filter(metric, selector):
    parts = ["metric.type = " + json.dumps(metric)]
    for key, value in sorted((selector or {}).get("dimensions", {}).items()):
        parts.append(f'metric.labels.{key} = {json.dumps(value)}')
    for key, value in sorted((selector or {}).get("resource_labels", {}).items()):
        parts.append(f'resource.labels.{key} = {json.dumps(value)}')
    return " AND ".join(parts)


def compare_metric_series(payload, config=None):
    config = load_observability_config(config)
    client = monitoring_client()
    interval = {"start_time": {"seconds": int(payload["start_time"])}, "end_time": {"seconds": int(payload["end_time"])}}
    request_base = {"name": project_name(config), "interval": interval, "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)}, "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN}, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL}
    left = client.list_time_series(request={**request_base, "filter": _build_filter(payload["metric"], payload.get("left"))})
    right = client.list_time_series(request={**request_base, "filter": _build_filter(payload["metric"], payload.get("right"))})
    return compare_series(left, right)
