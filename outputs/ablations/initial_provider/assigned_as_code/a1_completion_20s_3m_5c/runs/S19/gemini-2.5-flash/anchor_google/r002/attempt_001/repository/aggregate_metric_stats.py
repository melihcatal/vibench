import json

from google.cloud import monitoring_v3
from observability_client import get_metric_service_client
from observability_models import format_time_interval, normalize_time_series_points


def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = get_metric_service_client()
    
    project_id = config['project_id']
    metric_type = payload['metric']
    start_time = payload['start_time']
    end_time = payload['end_time']
    aggregation_period_seconds = payload.get('aggregation_period_seconds', 60)
    per_series_aligner = getattr(monitoring_v3.Aggregation.Aligner, payload.get('aligner', 'ALIGN_MEAN').upper())
    reducer = getattr(monitoring_v3.Aggregation.Reducer, payload.get('reducer', 'REDUCE_MEAN').upper())

    series = client.list_time_series(request={
        "name": f"projects/{project_id}",
        "filter": "metric.type = " + json.dumps(metric_type),
        "interval": format_time_interval(start_time, end_time),
        "aggregation": {
            "alignment_period": {"seconds": aggregation_period_seconds},
            "per_series_aligner": per_series_aligner,
            "cross_series_reducer": reducer,
            "group_by_fields": ["metric.labels.instance_name"] # Example grouping
        },
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    })
    
    points = normalize_time_series_points(series)
    return {"points": points}
