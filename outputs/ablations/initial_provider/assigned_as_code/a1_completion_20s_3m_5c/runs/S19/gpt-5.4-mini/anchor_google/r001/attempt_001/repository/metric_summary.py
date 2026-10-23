import json

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, load_observability_config, metric_project_name
from observability_models import summarize_points


def metric_summary(payload, config=None):
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
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind in ("double_value", "int64_value"):
                points.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})
    summary = summarize_points(sorted(points, key=lambda p: p["timestamp"]))
    if summary["count"] >= 2:
        summary["trend"] = "up" if summary["latest"]["value"] > summary["min"] else "flat"
    else:
        summary["trend"] = "insufficient-data"
    return summary
