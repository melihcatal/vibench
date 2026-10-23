from datetime import datetime
from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import MetricQueryRequest, MetricStatsResponse

def aggregate_metric_stats(request: MetricQueryRequest) -> MetricStatsResponse:
    client = ObservabilityClient().get_monitoring_client()
    project_name = f"projects/{request.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(request.end_time.timestamp())},
        start_time={'seconds': int(request.start_time.timestamp())}
    )

    query_filter = request.filter if request.filter else f'metric.type = "{request.metric_type}"'

    # Aggregation for statistics
    aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': int((request.end_time - request.start_time).total_seconds())},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=['metric.type']
    )

    # Fetch time series for average
    avg_results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation
    )

    average_value = None
    if avg_results:
        for ts in avg_results:
            for point in ts.points:
                value = point.int64_value or point.double_value or point.string_value or (point.bool_value if isinstance(point.bool_value, bool) else None)
                if value is not None:
                    average_value = float(value)
                    break
            if average_value is not None:
                break

    # For min, max, sum, count, we need separate queries with different reducers
    min_value, max_value, sum_value, count_value = None, None, None, None

    # Min aggregation
    min_aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': int((request.end_time - request.start_time).total_seconds())},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MIN,
        group_by_fields=['metric.type']
    )
    min_results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=min_aggregation
    )
    if min_results:
        for ts in min_results:
            for point in ts.points:
                value = point.int64_value or point.double_value or point.string_value or (point.bool_value if isinstance(point.bool_value, bool) else None)
                if value is not None:
                    min_value = float(value)
                    break
            if min_value is not None:
                break

    # Max aggregation
    max_aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': int((request.end_time - request.start_time).total_seconds())},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MAX,
        group_by_fields=['metric.type']
    )
    max_results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=max_aggregation
    )
    if max_results:
        for ts in max_results:
            for point in ts.points:
                value = point.int64_value or point.double_value or point.string_value or (point.bool_value if isinstance(point.bool_value, bool) else None)
                if value is not None:
                    max_value = float(value)
                    break
            if max_value is not None:
                break

    # Sum aggregation
    sum_aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': int((request.end_time - request.start_time).total_seconds())},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
        group_by_fields=['metric.type']
    )
    sum_results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=sum_aggregation
    )
    if sum_results:
        for ts in sum_results:
            for point in ts.points:
                value = point.int64_value or point.double_value or point.string_value or (point.bool_value if isinstance(point.bool_value, bool) else None)
                if value is not None:
                    sum_value = float(value)
                    break
            if sum_value is not None:
                break

    # Count aggregation
    count_aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': int((request.end_time - request.start_time).total_seconds())},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_COUNT,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
        group_by_fields=['metric.type']
    )
    count_results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=count_aggregation
    )
    if count_results:
        for ts in count_results:
            for point in ts.points:
                value = point.int64_value or point.double_value or point.string_value or (point.bool_value if isinstance(point.bool_value, bool) else None)
                if value is not None:
                    count_value = int(value)
                    break
            if count_value is not None:
                break

    return MetricStatsResponse(
        metric_type=request.metric_type,
        start_time=request.start_time,
        end_time=request.end_time,
        average=average_value,
        min=min_value,
        max=max_value,
        sum=sum_value,
        count=count_value
    )
