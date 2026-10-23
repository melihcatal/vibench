import json

from google.cloud import monitoring_v3

from observability_client import load_config, monitoring_client
from observability_models import normalize_metric_query, points_to_series


def _series(payload, config, selector_key):
    selectors = payload.get(selector_key, {})
    dimension_filter = " AND ".join([f'metric.label."{key}" = {json.dumps(value)}' for key, value in selectors.items()])
    metric_filter = "metric.type = " + json.dumps(payload["metric"])
    full_filter = metric_filter if not dimension_filter else metric_filter + " AND " + dimension_filter
    client = monitoring_client()
    series = client.list_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": full_filter,
        "interval": {"start_time": {"seconds": payload["start_time"]}, "end_time": {"seconds": payload["end_time"]}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    points = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})
    return points_to_series(points)


def compare_metric_series(payload, config=None):
    config = load_config(config)
    payload = normalize_metric_query(payload)
    left = _series(payload, config, "left_dimensions")
    right = _series(payload, config, "right_dimensions")
    return {"left": left, "right": right}
