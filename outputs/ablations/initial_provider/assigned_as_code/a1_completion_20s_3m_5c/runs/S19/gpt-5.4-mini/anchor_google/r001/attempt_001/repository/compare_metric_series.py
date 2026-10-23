import json

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, load_observability_config, metric_project_name
from observability_models import compare_series, normalize_scalar_points


def compare_metric_series(payload, config=None):
    config = load_observability_config(config)
    client = get_monitoring_client()
    base = {"name": metric_project_name(config["project_id"]),
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                     "end_time": {"seconds": int(payload["end_time"])}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL}
    left_request = dict(base)
    left_request["filter"] = "metric.type = " + json.dumps(payload["metric"]) + " AND " + payload["left_filter"]
    right_request = dict(base)
    right_request["filter"] = "metric.type = " + json.dumps(payload["metric"]) + " AND " + payload["right_filter"]
    left_points = normalize_scalar_points(client.list_time_series(request=left_request))
    right_points = normalize_scalar_points(client.list_time_series(request=right_request))
    return compare_series(left_points, right_points)
