from google.cloud import monitoring_v3
from observability_client import get_metrics_client
from observability_models import MetricQuery, MetricDatapoint, MetricQueryResult


def query_metric_window(query: MetricQuery) -> MetricQueryResult:
    client = get_metrics_client()
    project_name = f"projects/{query.project_id}"

    interval = monitoring_v3.TimeInterval(
        start_time={'seconds': int(query.interval_start_time)},
        end_time={'seconds': int(query.interval_end_time)},
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': int(query.period.rstrip('s'))},
        per_series_aligner=getattr(monitoring_v3.Aggregation.Aligner, query.aligner),
        cross_series_reducer=getattr(monitoring_v3.Aggregation.Reducer, query.reducer),
        group_by_fields=query.filters,
    )

    results = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{query.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    datapoints = []
    metric_name = query.metric_type

    for series in results:
        metric_name = series.metric.type
        for point in series.points:
            timestamp = point.interval.end_time.seconds
            value = point.value.double_value or point.value.int64_value
            labels = dict(series.metric.labels)
            datapoints.append(MetricDatapoint(str(timestamp), value, labels))

    return MetricQueryResult(metric_name, datapoints)
