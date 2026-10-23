import json

from google.cloud import monitoring_v3


def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = monitoring_v3.MetricServiceClient()
    series = client.list_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric"]),
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                      "end_time": {"seconds": int(payload["end_time"])}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                          "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    stats = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            stats.append(float(getattr(point.value, kind)))
    return {"count": len(stats), "mean": sum(stats) / len(stats) if stats else 0, "max": max(stats) if stats else 0, "min": min(stats) if stats else 0}
