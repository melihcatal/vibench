import datetime
from typing import Optional
from google.cloud import monitoring_v3
from observability_client import MonitoringClient
from observability_models import MetricQuery, MetricStatistics


def aggregate_metric_stats(query: MetricQuery) -> Optional[MetricStatistics]:
    client = MonitoringClient()
    metric_service_client = client.get_metric_service_client()
    project_name = client.get_project_name()

    interval = monitoring_v3.TimeInterval(
        end_time=query.end_time.timestamp(),
        start_time=query.start_time.timestamp(),
    )

    # Fetch mean
    aggregation_mean = monitoring_v3.Aggregation(
        alignment_period={"seconds": query.interval_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["metric.type"],
    )
    results_mean = metric_service_client.list_time_series(
        name=project_name,
        filter=f'metric.type="{query.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation_mean,
    )
    mean_value = None
    for series in results_mean:
        for point in series.points:
            mean_value = point.value.double_value or point.value.int64_value
            break
        if mean_value is not None:
            break

    # Fetch max
    aggregation_max = monitoring_v3.Aggregation(
        alignment_period={"seconds": query.interval_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MAX,
        group_by_fields=["metric.type"],
    )
    results_max = metric_service_client.list_time_series(
        name=project_name,
        filter=f'metric.type="{query.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation_max,
    )
    max_value = None
    for series in results_max:
        for point in series.points:
            max_value = point.value.double_value or point.value.int64_value
            break
        if max_value is not None:
            break

    # Fetch min
    aggregation_min = monitoring_v3.Aggregation(
        alignment_period={"seconds": query.interval_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MIN,
        group_by_fields=["metric.type"],
    )
    results_min = metric_service_client.list_time_series(
        name=project_name,
        filter=f'metric.type="{query.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation_min,
    )
    min_value = None
    for series in results_min:
        for point in series.points:
            min_value = point.value.double_value or point.value.int64_value
            break
        if min_value is not None:
            break

    # Fetch sum
    aggregation_sum = monitoring_v3.Aggregation(
        alignment_period={"seconds": query.interval_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
        group_by_fields=["metric.type"],
    )
    results_sum = metric_service_client.list_time_series(
        name=project_name,
        filter=f'metric.type="{query.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation_sum,
    )
    sum_value = None
    for series in results_sum:
        for point in series.points:
            sum_value = point.value.double_value or point.value.int64_value
            break
        if sum_value is not None:
            break

    # Fetch count
    aggregation_count = monitoring_v3.Aggregation(
        alignment_period={"seconds": query.interval_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_COUNT,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
        group_by_fields=["metric.type"],
    )
    results_count = metric_service_client.list_time_series(
        name=project_name,
        filter=f'metric.type="{query.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation_count,
    )
    count_value = None
    for series in results_count:
        for point in series.points:
            count_value = point.value.int64_value
            break
        if count_value is not None:
            break

    if any([mean_value, max_value, min_value, sum_value, count_value]):
        return MetricStatistics(
            metric_type=query.metric_type,
            start_time=query.start_time,
            end_time=query.end_time,
            mean=mean_value,
            max=max_value,
            min=min_value,
            sum=sum_value,
            count=count_value,
        )
    return None
