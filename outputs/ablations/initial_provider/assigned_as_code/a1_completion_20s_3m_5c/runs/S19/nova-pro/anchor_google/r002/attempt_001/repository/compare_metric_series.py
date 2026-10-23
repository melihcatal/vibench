import json

from google.cloud import monitoring_v3

def compare_metric_series(payload, config=None):
    config = config or {}
    client = monitoring_v3.MetricServiceClient()
    series1 = client.list_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric1"]),
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                       "end_time": {"seconds": int(payload["end_time"])}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                          "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    series2 = client.list_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric2"]),
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                       "end_time": {"seconds": int(payload["end_time"])}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                          "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    points1 = []
    points2 = []
    for timeseries in series1:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points1.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})
    for timeseries in series2:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points2.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})
    return {"series1": sorted(points1, key=lambda p: p["timestamp"]),
            "series2": sorted(points2, key=lambda p: p["timestamp"])}