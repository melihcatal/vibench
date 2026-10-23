import json

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, load_observability_config, metric_project_name
from observability_models import summarize_points


def aggregate_metric_stats(payload, config=None):
    config = load_observability_config(config)
    client = get_monitoring_client()
    series = client.list_time_series(request={"name": metric_project_name(config["project_id"]),
        "filter": "metric.type = " + json.dumps(payload["metric"]),
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                     "end_time": {"seconds": int(payload["end_time"])}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    points = []
    for timeseries in series:
        points.extend([{"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, point.value._pb.WhichOneof("value")))} for point in timeseries.points if point.value._pb.WhichOneof("value") in ("double_value", "int64_value")])
    return summarize_points(sorted(points, key=lambda p: p["timestamp"]))
