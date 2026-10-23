from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def get_aggregated_metric_stats(
    project_id: str,
    metric_type: str,
    end_time_seconds: int,
    duration_seconds: int,
):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = timestamp_pb2.Timestamp()
    now.seconds = end_time_seconds

    start_time = timestamp_pb2.Timestamp()
    start_time.seconds = end_time_seconds - duration_seconds

    interval = monitoring_v3.TimeInterval(end_time=now, start_time=start_time)

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 600},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["resource.zone", "metric.labels.instance_name"],
    )

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=f'''metric.type = "{metric_type}"''',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    response = client.list_time_series(request)

    results = []
    for series in response.time_series:
        for point in series.points:
            results.append({
                "start_time": point.interval.start_time.seconds,
                "end_time": point.interval.end_time.seconds,
                "value": point.value.double_value,
                "metric_labels": dict(series.metric.labels),
                "resource_labels": dict(series.resource.labels),
            })
    return results