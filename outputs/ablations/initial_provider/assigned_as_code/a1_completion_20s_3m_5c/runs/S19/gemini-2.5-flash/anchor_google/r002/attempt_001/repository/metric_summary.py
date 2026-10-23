import json

from google.cloud import monitoring_v3
from observability_client import get_metric_service_client
from observability_models import format_time_interval


def metric_summary(payload, config=None):
    config = config or {}
    client = get_metric_service_client()

    project_id = config['project_id']
    metric_type = payload['metric']
    start_time = payload['start_time']
    end_time = payload['end_time']
    summary_aligner = getattr(monitoring_v3.Aggregation.Aligner, payload.get('summary_aligner', 'ALIGN_MEAN').upper())
    summary_reducer = getattr(monitoring_v3.Aggregation.Reducer, payload.get('summary_reducer', 'REDUCE_MEAN').upper())
    summary_period_seconds = payload.get('summary_period_seconds', 3600) # e.g., hourly summary

    # Get aggregated data for a summary
    series = client.list_time_series(request={
        "name": f"projects/{project_id}",
        "filter": "metric.type = " + json.dumps(metric_type),
        "interval": format_time_interval(start_time, end_time),
        "aggregation": {
            "alignment_period": {"seconds": summary_period_seconds},
            "per_series_aligner": summary_aligner,
            "cross_series_reducer": summary_reducer,
            "group_by_fields": ["metric.labels.instance_name"] # Example grouping
        },
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    })

    summary_data = []
    for ts in series:
        for point in ts.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            summary_data.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})

    # Simple summary logic
    if not summary_data:
        return {"summary": "No data available for the specified period."}

    values = [p["value"] for p in summary_data]
    avg_value = sum(values) / len(values) if values else 0
    max_value = max(values) if values else 0
    min_value = min(values) if values else 0

    return {
        "summary": f"Metric: {metric_type}, Average: {avg_value:.2f}, Max: {max_value:.2f}, Min: {min_value:.2f}",
        "details": summary_data
    }
