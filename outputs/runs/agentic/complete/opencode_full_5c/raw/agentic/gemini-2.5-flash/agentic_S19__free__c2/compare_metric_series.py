from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import (
    MetricQuery,
    MetricQueryResponse,
    TimeSeries,
    TimeSeriesPoint,
)


def compare_metric_series(
    query1: MetricQuery, query2: MetricQuery
) -> Dict[str, MetricQueryResponse]:
    client = get_monitoring_client()
    project_name = f"projects/{query1.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(query1.interval_end_time)},
        start_time={"seconds": int(query1.interval_start_time)},
    )

    # Query for the first series
    filter1 = f'metric.type = "{query1.metric_type}" AND {query1.filter}'
    result1 = client.list_time_series(
        name=project_name,
        filter=filter1,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    time_series_list1 = []
    for ts in result1:
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
        time_series_list1.append(
            TimeSeries(
                metric=ts.metric.labels, resource=ts.resource.labels, points=points
            )
        )
    response1 = MetricQueryResponse(time_series=time_series_list1)

    # Query for the second series
    filter2 = f'metric.type = "{query2.metric_type}" AND {query2.filter}'
    result2 = client.list_time_series(
        name=project_name,
        filter=filter2,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    time_series_list2 = []
    for ts in result2:
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
        time_series_list2.append(
            TimeSeries(
                metric=ts.metric.labels, resource=ts.resource.labels, points=points
            )
        )
    response2 = MetricQueryResponse(time_series=time_series_list2)

    return {"series1": response1, "series2": response2}


from typing import Dict

if __name__ == "__main__":
    project_id = get_project_id()
    end_time = 1678886400  # Example timestamp (March 15, 2023 12:00:00 PM UTC)
    start_time = end_time - 3600  # 1 hour before

    # Example usage: compare CPU utilization for two different instances
    query1 = MetricQuery(
        project_id=project_id,
        metric_type="compute.googleapis.com/instance/cpu/utilization",
        interval_end_time=str(end_time),
        interval_start_time=str(start_time),
        filter='resource.labels.instance_id = "1234567890"',
    )
    query2 = MetricQuery(
        project_id=project_id,
        metric_type="compute.googleapis.com/instance/cpu/utilization",
        interval_end_time=str(end_time),
        interval_start_time=str(start_time),
        filter='resource.labels.instance_id = "0987654321"',
    )

    responses = compare_metric_series(query1, query2)
    print("Compare Metric Series Response:")
    print("Series 1:")
    for ts in responses["series1"].time_series:
        print(f"  Metric: {ts.metric}, Resource: {ts.resource}")
        for point in ts.points:
            print(f"    Timestamp: {point.timestamp}, Value: {point.value}")

    print("\nSeries 2:")
    for ts in responses["series2"].time_series:
        print(f"  Metric: {ts.metric}, Resource: {ts.resource}")
        for point in ts.points:
            print(f"    Timestamp: {point.timestamp}, Value: {point.value}")
