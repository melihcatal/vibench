import json

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, load_observability_config, metric_project_name
from observability_models import normalize_scalar_points


def filter_metric_dimensions(payload, config=None):
    config = load_observability_config(config)
    filters = payload.get("dimensions", {})
    dimension_filter = " AND ".join([f'{key} = {json.dumps(value)}' for key, value in sorted(filters.items())])
    metric_filter = "metric.type = " + json.dumps(payload["metric"])
    request_filter = metric_filter if not dimension_filter else metric_filter + " AND " + dimension_filter
    client = get_monitoring_client()
    series = client.list_time_series(request={"name": metric_project_name(config["project_id"]),
        "filter": request_filter,
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                     "end_time": {"seconds": int(payload["end_time"])}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    return {"points": normalize_scalar_points(series)}
