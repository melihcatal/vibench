from datetime import datetime
from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import MetricQueryRequest, MetricComparisonResponse, TimeSeries, TimeSeriesPoint

def compare_metric_series(request_a: MetricQueryRequest, request_b: MetricQueryRequest) -> MetricComparisonResponse:
    client = ObservabilityClient().get_monitoring_client()
    project_name = f"projects/{request_a.project_id}"

    # Ensure both requests have the same time window
    if not (request_a.start_time == request_b.start_time and request_a.end_time == request_b.end_time):
        raise ValueError("Comparison requests must have the same start and end times.")

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(request_a.end_time.timestamp())},
        start_time={'seconds': int(request_a.start_time.timestamp())}
    )

    def fetch_time_series(req: MetricQueryRequest) -> TimeSeries:
        query_filter = req.filter if req.filter else f'metric.type = "{req.metric_type}"'

        aggregation = monitoring_v3.Aggregation()
        if req.interval_minutes:
            aggregation.alignment_period = {'seconds': req.interval_minutes * 60}
            aggregation.per_series_aligner = (getattr(monitoring_v3.Aggregation.Aligner, req.aligner) if req.aligner
                                             else monitoring_v3.Aggregation.Aligner.ALIGN_MEAN)
        if req.reducer:
            aggregation.cross_series_reducer = getattr(monitoring_v3.Aggregation.Reducer, req.reducer)
        if req.group_by:
            aggregation.group_by_fields.extend(req.group_by)

        results = client.list_time_series(
            name=project_name,
            filter=query_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            aggregation=aggregation
        )

        # For comparison, we expect a single time series or we pick the first one
        if not results:
            return TimeSeries(metric_labels={}, resource_labels={}, points=[])
        
        ts = list(results)[0]
        points = []
        for point in ts.points:
            value = point.int64_value or point.double_value or point.string_value or (point.bool_value if isinstance(point.bool_value, bool) else None)
            if value is not None:
                points.append(TimeSeriesPoint(
                    timestamp=datetime.fromtimestamp(point.interval.end_time.seconds),
                    value=float(value)
                ))
        return TimeSeries(
            metric_labels=dict(ts.metric.labels),
            resource_labels=dict(ts.resource.labels),
            points=points
        )

    series_a = fetch_time_series(request_a)
    series_b = fetch_time_series(request_b)

    # Perform a simple comparison, e.g., average difference
    difference = None
    percentage_difference = None

    if series_a.points and series_b.points:
        avg_a = sum(p.value for p in series_a.points) / len(series_a.points)
        avg_b = sum(p.value for p in series_b.points) / len(series_b.points)

        difference = avg_a - avg_b
        if avg_b != 0:
            percentage_difference = (difference / avg_b) * 100

    return MetricComparisonResponse(
        metric_type=request_a.metric_type, # Assuming same metric type for comparison
        start_time=request_a.start_time,
        end_time=request_a.end_time,
        series_a=series_a,
        series_b=series_b,
        difference=difference,
        percentage_difference=percentage_difference
    )
