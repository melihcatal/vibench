from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_metric_service_client
from observability_models import MetricQuery, MetricResponse, TimeSeries, TimeSeriesPoint

def query_metric_window(query: MetricQuery) -> MetricResponse:
    """Queries recent datapoints for a named metric over a time window.

    Provider: Google Cloud Monitoring
    """
    client = get_metric_service_client()
    project_name = f"projects/{query.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time=Timestamp(seconds=int(query.interval_end_time)),
        start_time=Timestamp(seconds=int(query.interval_start_time)),
    )

    # Provider-identifying signal: google.cloud.monitoring_v3.MetricServiceClient.list_time_series
    # Provider-identifying signal: metrics.type like 'compute.googleapis.com/instance/cpu/usage_time'
    response = client.list_time_series(
        name=project_name,
        filter=query.filter or f'metric.type = "{query.metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    time_series_list = []
    for ts_proto in response.time_series:
        points = [
            TimeSeriesPoint(value=p.value.double_value or p.value.int64_value or p.value.string_value or p.value.bool_value, timestamp=str(p.interval.end_time.seconds))
            for p in ts_proto.points
        ]
        time_series_list.append(
            TimeSeries(
                metric=dict(ts_proto.metric.labels),
                resource=dict(ts_proto.resource.labels),
                points=points,
                metric_kind=monitoring_v3.MetricDescriptor.MetricKind(ts_proto.metric_kind).name,
                value_type=monitoring_v3.MetricDescriptor.ValueType(ts_proto.value_type).name,
            )
        )
    return MetricResponse(time_series=time_series_list)
