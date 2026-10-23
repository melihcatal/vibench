import json

from google.cloud import monitoring_v3

def filter_metric_dimensions(payload, config=None):
    config = config or {}
    client = monitoring_v3.MetricServiceClient()
    series = client.list_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric"]) + " AND resource.label." + json.dumps(payload["dimension"]) + " = " + json.dumps(payload["value"]),
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                       "end_time": {"seconds": int(payload["end_time"])}},
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
    return {"points": sorted(points, key=lambda p: p["timestamp"])}