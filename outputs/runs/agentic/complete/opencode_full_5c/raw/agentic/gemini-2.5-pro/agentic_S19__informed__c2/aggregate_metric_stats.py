import time
from google.cloud import monitoring_v3
from observability_client import get_gcp_observability_client, get_gcp_project_name
from observability_models import AggregationRequest, MetricTimeSeries, TimeSeriesPoint


def aggregate_metric_stats(request: AggregationRequest) -> list[MetricTimeSeries]:
    client = get_gcp_observability_client(request.project_id)
    if not client:
        return []

    project_name = get_gcp_project_name(request.project_id)
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {
                "seconds": seconds - (request.minutes_ago * 60),
                "nanos": nanos,
            },
        }
    )

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": request.alignment_period_seconds},
            "per_series_aligner": getattr(
                monitoring_v3.Aggregation.Aligner, request.per_series_aligner
            ),
            "cross_series_reducer": getattr(
                monitoring_v3.Aggregation.Reducer, request.cross_series_reducer
            ),
            "group_by_fields": ["metric.labels.zone"],
        }
    )

    filter_str = f'metric.type = "{request.metric_name}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    aggregated_data = []
    for result in results:
        points = []
        for point in result.points:
            points.append(
                TimeSeriesPoint(
                    timestamp=point.interval.end_time.rfc3339(),
                    value=point.value.double_value,
                )
            )

        dimensions = {
            label: result.metric.labels[label] for label in result.metric.labels
        }

        aggregated_data.append(
            MetricTimeSeries(
                metric_name=result.metric.type, dimensions=dimensions, points=points
            )
        )
    return aggregated_data
