from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import (
    MetricQuery,
    MetricQueryResponse,
    TimeSeries,
    TimeSeriesPoint,
)


def aggregate_metric_stats(query: MetricQuery) -> MetricQueryResponse:
    client = get_monitoring_client()
    project_name = f"projects/{query.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(query.interval_end_time)},
        start_time={"seconds": int(query.interval_start_time)},
    )

    # Example filter, adjust based on actual metric needs
    metric_filter = f'metric.type = "{query.metric_type}"'
    if query.filter:
        metric_filter += f" AND {query.filter}"

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": query.aggregation_period_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=query.group_by_fields,
    )

    result = client.list_time_series(
        name=project_name,
        filter=metric_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    time_series_list = []
    for ts in result:
        points = []
        for point in ts.points:
            value = None
            if point.value.double_value:
                value = point.value.double_value
            elif point.value.int64_value:
                value = point.value.int64_value
            elif point.value.bool_value:
                value = point.value.bool_value
            elif point.value.string_value:
                value = point.value.string_value

            points.append(
                TimeSeriesPoint(value=value, timestamp=point.interval.end_time.seconds)
            )
        time_series_list.append(
            TimeSeries(
                metric=ts.metric.labels, resource=ts.resource.labels, points=points
            )
        )

    return MetricQueryResponse(time_series=time_series_list)


if __name__ == "__main__":
    project_id = get_project_id()
    end_time = 1678886400  # Example timestamp (March 15, 2023 12:00:00 PM UTC)
    start_time = end_time - 3600  # 1 hour before

    # Example usage: aggregate average CPU utilization for all GCE instances
    metric_query = MetricQuery(
        project_id=project_id,
        metric_type="compute.googleapis.com/instance/cpu/utilization",
        interval_end_time=str(end_time),
        interval_start_time=str(start_time),
        aggregation_period_seconds=300,  # 5 minutes aggregation
        group_by_fields=["resource.instance_id"],
    )

    response = aggregate_metric_stats(metric_query)
    print("Aggregate Metric Stats Response:")
    for ts in response.time_series:
        print(f"  Metric: {ts.metric}, Resource: {ts.resource}")
        for point in ts.points:
            print(f"    Timestamp: {point.timestamp}, Value: {point.value}")
