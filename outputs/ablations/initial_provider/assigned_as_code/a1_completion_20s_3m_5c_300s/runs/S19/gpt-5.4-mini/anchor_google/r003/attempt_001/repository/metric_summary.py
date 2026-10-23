import json

from google.cloud import monitoring_v3

from observability_client import load_observability_config, monitoring_client, project_name


def metric_summary(payload, config=None):
    config = load_observability_config(config)
    client = monitoring_client()
    series = client.list_time_series(request={"name": project_name(config), "filter": "metric.type = " + json.dumps(payload["metric"]), "interval": {"start_time": {"seconds": int(payload["start_time"])}, "end_time": {"seconds": int(payload["end_time"])}}, "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)}, "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN}, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    values = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind in ("double_value", "int64_value"):
                values.append(float(getattr(point.value, kind)))
    if not values:
        return {"trend": "flat", "anomalies": [], "count": 0}
    first = values[0]
    last = values[-1]
    return {"trend": "up" if last > first else "down" if last < first else "flat", "anomalies": [v for v in values if v > sum(values) / len(values) * 1.5 or v < sum(values) / len(values) * 0.5], "count": len(values)}
