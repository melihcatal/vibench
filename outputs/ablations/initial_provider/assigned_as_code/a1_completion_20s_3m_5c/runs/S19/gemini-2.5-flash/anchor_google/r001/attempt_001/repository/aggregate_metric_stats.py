import json

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import MetricPoint

def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = get_monitoring_client()

    # Default aggregation to MEAN and REDUCE_MEAN if not provided
    aligner = getattr(monitoring_v3.Aggregation.Aligner, payload.get("aligner", "ALIGN_MEAN").upper())
    reducer = getattr(monitoring_v3.Aggregation.Reducer, payload.get("reducer", "REDUCE_MEAN").upper())

    aggregation = {
        "alignment_period": {"seconds": config.get("period_seconds", 60)},
        "per_series_aligner": aligner,
        "cross_series_reducer": reducer,
        "group_by_fields": payload.get("group_by_fields", [])
    }

    series = client.list_time_series(request={
        "name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric"]),
        "interval": {
            "start_time": {"seconds": int(payload["start_time"])
            },
            "end_time": {"seconds": int(payload["end_time"])}
        },
        "aggregation": aggregation,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    })

    aggregated_data = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            aggregated_data.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})
    return {"aggregated_points": sorted(aggregated_data, key=lambda p: p["timestamp"])}
