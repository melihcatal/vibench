import json

from google.cloud import monitoring_v3

from observability_client import load_config, monitoring_client
from observability_models import normalize_metric_query, points_to_series


def metric_summary(payload, config=None):
    config = load_config(config)
    payload = normalize_metric_query(payload)
    client = monitoring_client()
    series = client.list_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric"]),
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
    points = points_to_series(points)
    if len(points) < 2:
        return {"trend": "insufficient_data", "points": points}
    delta = points[-1]["value"] - points[0]["value"]
    return {"trend": "up" if delta > 0 else "down" if delta < 0 else "flat", "delta": delta, "points": points}
