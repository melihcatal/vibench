from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import MetricRequest, MetricResponse, TimeSeries, TimeSeriesPoint
from google.protobuf import timestamp_pb2

def query_metric_window(request: MetricRequest) -> MetricResponse:
    client = ObservabilityClient().get_metric_service_client()
    project_name = f"projects/{request.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time=timestamp_pb2.Timestamp(seconds=int(request.interval_end)),
        start_time=timestamp_pb2.Timestamp(seconds=int(request.interval_start)),
    )

    query_filter = f'metric.type = "{request.metric_type}"'
    if request.filter_str:
        query_filter += f' AND {request.filter_str}'

    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    time_series_list = []
    for ts in response.time_series:
        points = []
        for point in ts.points:
            value = None
            if point.value.double_value:
                value = point.value.double_value
            elif point.value.int64_value:
                value = point.value.int64_value
            elif point.value.string_value:
                value = point.value.string_value
            elif point.value.bool_value:
                value = point.value.bool_value
            points.append(TimeSeriesPoint(value=value, timestamp=point.interval.end_time.ToJsonString()))

        time_series_list.append(TimeSeries(
            metric_labels=dict(ts.metric.labels),
            resource_labels=dict(ts.resource.labels),
            points=points
        ))
    return MetricResponse(time_series=time_series_list)