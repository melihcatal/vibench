import json

from google.cloud import monitoring_v3

from observability_client import load_observability_config, monitoring_client, project_name
from observability_models import normalize_points


def compare_metric_series(payload, config=None):
    config = load_observability_config(config)
    client = monitoring_client()
    results = {}
    for key in ("left", "right"):
        selector = payload[key]
        dimension_filter = selector.get("dimension_filter", {})
        dimension_query = " and ".join([f'{k} = {json.dumps(v)}' for k, v in sorted(dimension_filter.items())])
        metric_filter = "metric.type = " + json.dumps(payload["metric"])
        full_filter = metric_filter if not dimension_query else metric_filter + " and " + dimension_query
        series = client.list_time_series(request={"name": project_name(config["project_id"]),
            "filter": full_filter,
            "interval": {"start_time": {"seconds": int(payload["start_time"])},
                         "end_time": {"seconds": int(payload["end_time"])}},
            "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
        results[key] = normalize_points(series)
    return results
