import json

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client, project_name
from observability_models import build_time_window, extract_scalar_value, normalize_points


def filter_metric_dimensions(payload, config=None):
    cfg = load_config(config)
    client = metric_client()
    dimension_filters = payload.get("dimensions", {})
    dimension_expr = " AND ".join([f'resource.labels.{key} = "{value}"' for key, value in dimension_filters.items()])
    metric_filter = "metric.type = " + json.dumps(payload["metric"])
    request_filter = metric_filter if not dimension_expr else metric_filter + " AND " + dimension_expr
    series = client.list_time_series(request={"name": project_name(cfg),
        "filter": request_filter,
        "interval": build_time_window(payload),
        "aggregation": {"alignment_period": {"seconds": cfg.period_seconds},
                        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    points = []
    for timeseries in series:
        for point in timeseries.points:
            points.append({"timestamp": point.interval.end_time.timestamp(), "value": extract_scalar_value(point)})
    return {"points": normalize_points(points)}
