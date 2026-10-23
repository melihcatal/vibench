import json

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import MetricPoint

def filter_metric_dimensions(payload, config=None):
    config = config or {}
    client = get_monitoring_client()

    metric_filter = "metric.type = " + json.dumps(payload["metric"])
    dimension_filters = []
    if "resource_labels" in payload:
        for key, value in payload["resource_labels"].items():
            dimension_filters.append(f"resource.labels.{key} = " + json.dumps(value))
    if "metric_labels" in payload:
        for key, value in payload["metric_labels"].items():
            dimension_filters.append(f"metric.labels.{key} = " + json.dumps(value))

    full_filter = metric_filter
    if dimension_filters:
        full_filter += " AND " + " AND ".join(dimension_filters)

    series = client.list_time_series(request={
        "name": f"projects/{config['project_id']}",
        "filter": full_filter,
        "interval": {
            "start_time": {"seconds": int(payload["start_time"])}
            ,
            "end_time": {"seconds": int(payload["end_time"])}
        },
        "aggregation": {
            "alignment_period": {"seconds": config.get("period_seconds", 60)},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
        },
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    })

    filtered_data = []
    for timeseries in series:
        points = []
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points.append(MetricPoint(timestamp=point.interval.end_time.timestamp(), value=float(getattr(point.value, kind))))

        resource_labels = {k: v for k, v in timeseries.resource.labels.items()}
        metric_labels = {k: v for k, v in timeseries.metric.labels.items()}
        
        filtered_data.append({
            "resource_labels": resource_labels,
            "metric_labels": metric_labels,
            "points": [p.__dict__ for p in points] # Convert MetricPoint to dict for serialization
        })

    return {"filtered_series": filtered_data}
