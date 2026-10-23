from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_metric_service_client
from observability_models import MetricQuery, MetricResponse, TimeSeries, TimeSeriesPoint

def compare_metric_series(query1: MetricQuery, query2: MetricQuery) -> dict:
    """Compares metric values for two resources or dimension filters over the same window.

    Provider: Google Cloud Monitoring
    """
    client = get_metric_service_client()
    project_name = f"projects/{query1.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time=Timestamp(seconds=int(query1.interval_end_time)),
        start_time=Timestamp(seconds=int(query1.interval_start_time)),
    )

    # Query for the first series
    # Provider-identifying signal: google.cloud.monitoring_v3.MetricServiceClient.list_time_series
    # Provider-identifying signal: metrics.type like 'compute.googleapis.com/instance/cpu/usage_time'
    response1 = client.list_time_series(
        name=project_name,
        filter=query1.filter or f'metric.type = "{query1.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    time_series_list1 = []
    for ts_proto in response1.time_series:
        points = [
            TimeSeriesPoint(value=p.value.double_value or p.value.int64_value or p.value.string_value or p.value.bool_value, timestamp=str(p.interval.end_time.seconds))
            for p in ts_proto.points
        ]
        time_series_list1.append(
            TimeSeries(
                metric=dict(ts_proto.metric.labels),
                resource=dict(ts_proto.resource.labels),
                points=points,
                metric_kind=monitoring_v3.MetricDescriptor.MetricKind(ts_proto.metric_kind).name,
                value_type=monitoring_v3.MetricDescriptor.ValueType(ts_proto.value_type).name,
            )
        )

    # Query for the second series
    response2 = client.list_time_series(
        name=project_name,
        filter=query2.filter or f'metric.type = "{query2.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    time_series_list2 = []
    for ts_proto in response2.time_series:
        points = [
            TimeSeriesPoint(value=p.value.double_value or p.value.int64_value or p.value.string_value or p.value.bool_value, timestamp=str(p.interval.end_time.seconds))
            for p in ts_proto.points
        ]
        time_series_list2.append(
            TimeSeries(
                metric=dict(ts_proto.metric.labels),
                resource=dict(ts_proto.resource.labels),
                points=points,
                metric_kind=monitoring_v3.MetricDescriptor.MetricKind(ts_proto.metric_kind).name,
                value_type=monitoring_v3.MetricDescriptor.ValueType(ts_proto.value_type).name,
            )
        )

    return {
        "series1": MetricResponse(time_series=time_series_list1),
        "series2": MetricResponse(time_series=time_series_list2),
    }
