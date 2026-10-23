from datetime import datetime
from google.cloud import monitoring_v3
from observability_client import get_metrics_client

def filter_metric_dimensions(payload: dict, config: dict = None):
    config = config or {}
    client = get_metrics_client()

    project_id = payload.get('project_id')
    metric_name = payload.get('metric_name')
    start_time = datetime.fromtimestamp(payload.get('start_time'))
    end_time = datetime.fromtimestamp(payload.get('end_time'))
    metric_filter = payload.get('filter') # e.g., 'resource.labels.instance_name="my-instance"'

    if not all([project_id, metric_name, start_time, end_time, metric_filter]):
        raise ValueError("Missing required payload parameters: project_id, metric_name, start_time, end_time, filter")

    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        start_time={'seconds': int(start_time.timestamp())},
        end_time={'seconds': int(end_time.timestamp())}
    )

    # Default aggregation to MEAN for filtered queries
    aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': payload.get('interval_seconds', 300)}, # Default to 5 minutes
        per_series_aligner=getattr(monitoring_v3.Aggregation.Aligner, payload.get('aggregation_aligner', 'ALIGN_MEAN')),
        cross_series_reducer=getattr(monitoring_v3.Aggregation.Reducer, payload.get('aggregation_reducer', 'REDUCE_NONE')) # No cross-series reduction initially to preserve dimensions
    )

    full_filter = f'metric.type = "{metric_name}" AND {metric_filter}'

    results = client.list_time_series(
        name=project_name,
        filter=full_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation
    )

    points = []
    for series in results:
        for point in series.points:
            points.append({
                'timestamp': point.interval.end_time.timestamp(),
                'value': point.value.double_value if point.value.value_type == monitoring_v3.TypedValue.ValueType.DOUBLE else \
                           point.value.int64_value if point.value.value_type == monitoring_v3.TypedValue.ValueType.INT64 else \
                           point.value.bool_value if point.value.value_type == monitoring_v3.TypedValue.ValueType.BOOL else \
                           str(point.value.string_value), # Fallback for STRING
                'metric_labels': dict(series.metric.labels),
                'resource_labels': dict(series.resource.labels)
            })

    return {'points': sorted(points, key=lambda point: point['timestamp'])}
