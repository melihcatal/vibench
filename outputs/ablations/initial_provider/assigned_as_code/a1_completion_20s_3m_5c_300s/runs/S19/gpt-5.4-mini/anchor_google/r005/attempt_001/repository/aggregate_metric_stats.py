import json

from google.cloud import monitoring_v3

from observability_client import load_config, monitoring_client
from observability_models import normalize_metric_query


def aggregate_metric_stats(payload, config=None):
    config = load_config(config)
    payload = normalize_metric_query(payload)
    client = monitoring_client()
    series = client.list_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric"]),
        "interval": {"start_time": {"seconds": payload["start_time"]}, "end_time": {"seconds": payload["end_time"]}},
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
                        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    values = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            values.append(float(getattr(point.value, kind)))
    if not values:
        return {"count": 0, "mean": None, "min": None, "max": None}
    return {"count": len(values), "mean": sum(values) / len(values), "min": min(values), "max": max(values)}
