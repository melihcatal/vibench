import os
import datetime
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricQuery, MetricSeries

def aggregate_metric_stats(query: MetricQuery) -> list[MetricSeries]:
    client = get_monitoring_client()
    project_name = f"projects/{query.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time=query.end_time,
        start_time=query.start_time,
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': query.agg_period_seconds},
        per_series_aligner=query.agg_aligner, # e.g., monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
        cross_series_reducer=query.agg_reducer, # e.g., monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
        group_by_fields=query.group_by_fields if hasattr(query, 'group_by_fields') else []
    )

    query_filter = f'metric.type = "{query.metric_type}"'
    if query.filter_string:
        query_filter += f' AND {query.filter_string}'

    response = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        aggregation=aggregation,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    all_series = []
    for ts in response:
        datapoints = []
        for point in ts.points:
            timestamp = point.interval.end_time.timestamp()
            value = point.value.double_value if point.value.value_type == monitoring_v3.TypedValue.ValueType.DOUBLE else \
                    point.value.int64_value if point.value.value_type == monitoring_v3.TypedValue.ValueType.INT64 else \
                    point.value.bool_value if point.value.value_type == monitoring_v3.TypedValue.ValueType.BOOL else None
            if value is not None:
                datapoints.append(MetricSeries.Datapoint(timestamp=timestamp, value=value))
        
        all_series.append(MetricSeries(
            resource_labels=dict(ts.resource.labels),
            metric_labels=dict(ts.metric.labels),
            datapoints=datapoints
        ))
    return all_series