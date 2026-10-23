from datetime import datetime
from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import MetricQueryRequest, MetricQueryResponse, TimeSeries, TimeSeriesPoint

def filter_metric_dimensions(request: MetricQueryRequest) -> MetricQueryResponse:
    client = ObservabilityClient().get_monitoring_client()
    project_name = f"projects/{request.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(request.end_time.timestamp())},
        start_time={'seconds': int(request.start_time.timestamp())}
    )

    # The filter is expected to be provided in the request for this function
    if not request.filter:
        raise ValueError("A filter string is required for filtering metric dimensions.")

    query_filter = request.filter

    aggregation = monitoring_v3.Aggregation()
    if request.interval_minutes:
        aggregation.alignment_period = {'seconds': request.interval_minutes * 60}
        aggregation.per_series_aligner = (getattr(monitoring_v3.Aggregation.Aligner, request.aligner) if request.aligner
                                         else monitoring_v3.Aggregation.Aligner.ALIGN_MEAN)
    if request.reducer:
        aggregation.cross_series_reducer = getattr(monitoring_v3.Aggregation.Reducer, request.reducer)
    if request.group_by:
        aggregation.group_by_fields.extend(request.group_by)

    results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation
    )

    time_series_list = []
    for ts in results:
        points = []
        for point in ts.points:
            value = point.int64_value or point.double_value or point.string_value or (point.bool_value if isinstance(point.bool_value, bool) else None)
            if value is not None:
                points.append(TimeSeriesPoint(
                    timestamp=datetime.fromtimestamp(point.interval.end_time.seconds),
                    value=float(value)
                ))
        time_series_list.append(TimeSeries(
            metric_labels=dict(ts.metric.labels),
            resource_labels=dict(ts.resource.labels),
            points=points
        ))

    return MetricQueryResponse(time_series=time_series_list)
