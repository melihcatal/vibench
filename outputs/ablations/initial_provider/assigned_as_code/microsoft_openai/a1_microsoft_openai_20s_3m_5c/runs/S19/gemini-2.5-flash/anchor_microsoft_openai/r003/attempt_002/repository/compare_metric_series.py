from datetime import datetime
from google.cloud import monitoring_v3
from observability_client import get_metrics_client

def _query_series(client, project_id, metric_name, start_time, end_time, metric_filter, interval_seconds, aggregation_aligner, aggregation_reducer):
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        start_time={'seconds': int(start_time.timestamp())},
        end_time={'seconds': int(end_time.timestamp())}
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': interval_seconds},
        per_series_aligner=getattr(monitoring_v3.Aggregation.Aligner, aggregation_aligner),
        cross_series_reducer=getattr(monitoring_v3.Aggregation.Reducer, aggregation_reducer)
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
                           str(point.value.string_value) # Fallback for STRING
            })
    return sorted(points, key=lambda point: point['timestamp'])

def compare_metric_series(payload: dict, config: dict = None):
    config = config or {}
    client = get_metrics_client()

    project_id = payload.get('project_id')
    metric_name = payload.get('metric_name')
    start_time = datetime.fromtimestamp(payload.get('start_time'))
    end_time = datetime.fromtimestamp(payload.get('end_time'))
    filter_a = payload.get('filter_a')
    filter_b = payload.get('filter_b')
    interval_seconds = payload.get('interval_seconds', 300)
    aggregation_aligner = payload.get('aggregation_aligner', 'ALIGN_MEAN')
    aggregation_reducer = payload.get('aggregation_reducer', 'REDUCE_MEAN')

    if not all([project_id, metric_name, start_time, end_time, filter_a, filter_b]):
        raise ValueError("Missing required payload parameters: project_id, metric_name, start_time, end_time, filter_a, filter_b")

    series_a_points = _query_series(client, project_id, metric_name, start_time, end_time, filter_a, interval_seconds, aggregation_aligner, aggregation_reducer)
    series_b_points = _query_series(client, project_id, metric_name, start_time, end_time, filter_b, interval_seconds, aggregation_aligner, aggregation_reducer)

    return {
        'series_a': series_a_points,
        'series_b': series_b_points
    }
