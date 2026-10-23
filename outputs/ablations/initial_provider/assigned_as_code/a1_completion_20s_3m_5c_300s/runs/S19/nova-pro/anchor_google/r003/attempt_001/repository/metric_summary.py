import json

from google.cloud import monitoring_v3


def metric_summary(payload, config=None):
    config = config or {}
    client = monitoring_v3.MetricServiceClient()
    series = client.list_time_series(request={"name": f"projects/{config['project_id']}",
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
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})
    if not points:
        return {"summary": "No data available"}
    sorted_points = sorted(points, key=lambda p: p["timestamp"])
    first_point = sorted_points[0]
    last_point = sorted_points[-1]
    trend = "increasing" if last_point["value"] > first_point["value"] else "decreasing"
    return {"summary": f"Trend is {trend} from {first_point['value']} to {last_point['value']}"}
