from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from observability_client import get_metrics_client

def metric_summary(payload: dict, config: dict = None):
    config = config or {}
    client = get_metrics_client()

    project_id = payload.get('project_id')
    metric_name = payload.get('metric_name')
    window_hours = payload.get('window_hours', 1) # Default to 1 hour summary

    if not all([project_id, metric_name]):
        raise ValueError("Missing required payload parameters: project_id, metric_name")

    project_name = f"projects/{project_id}"
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=window_hours)

    interval = monitoring_v3.TimeInterval(
        start_time={'seconds': int(start_time.timestamp())},
        end_time={'seconds': int(end_time.timestamp())}
    )

    # Aggregate to get a single value per series for summary
    aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': window_hours * 3600}, # Align over the entire window
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=[] # Aggregate all series into one result for a summary
    )

    results = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_name}" {payload.get('filter', '')}',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation
    )

    summary_value = None
    if results:
        # Assuming there's only one time series after aggregation and reduction
        for series in results:
            if series.points:
                point = series.points[0] # Get the single aggregated point
                summary_value = point.value.double_value if point.value.value_type == monitoring_v3.TypedValue.ValueType.DOUBLE else \
                                point.value.int64_value if point.value.value_type == monitoring_v3.TypedValue.ValueType.INT64 else \
                                point.value.bool_value if point.value.value_type == monitoring_v3.TypedValue.ValueType.BOOL else \
                                str(point.value.string_value)
                break

    # In a real scenario, you'd do more sophisticated anomaly detection or trend analysis here.
    # For this example, we'll just return the aggregated mean value as a simple summary.
    return {'summary_value': summary_value, 'metric_name': metric_name, 'window_hours': window_hours}
