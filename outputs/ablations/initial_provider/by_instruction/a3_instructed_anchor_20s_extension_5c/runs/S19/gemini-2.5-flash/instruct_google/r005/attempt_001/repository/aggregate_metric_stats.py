import datetime
import os
from typing import List, Dict, Any

from google.cloud import monitoring_v3

from observability_client import ObservabilityClient
from observability_models import MetricDataPoint, MetricQueryResult

def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    alignment_period_seconds: int = 300,  # 5 minutes
    reducer: monitoring_v3.Aggregation.Aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
) -> List[MetricQueryResult]:
    client = ObservabilityClient(project_id)
    monitoring_client = client.get_monitoring_client()
    project_name = client.get_project_name()

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat(timespec="seconds") + "Z",
        start_time=start_time.isoformat(timespec="seconds") + "Z",
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": alignment_period_seconds},
        per_series_aligner=reducer,
    )

    query_results = []

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    page_iterator = monitoring_client.list_time_series(request=request)

    for series in page_iterator:
        metric_name = series.metric.type
        resource_labels = dict(series.resource.labels)
        points = []
        for point in series.points:
            timestamp = point.interval.end_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
            value = point.value.double_value if point.value.WhichOneof("value_type") == "double_value" else point.value.int64_value
            points.append(MetricDataPoint(timestamp=timestamp, value=value, labels=dict(series.metric.labels)))
        query_results.append(MetricQueryResult(metric_name=metric_name, resource_labels=resource_labels, points=points))

    return query_results
