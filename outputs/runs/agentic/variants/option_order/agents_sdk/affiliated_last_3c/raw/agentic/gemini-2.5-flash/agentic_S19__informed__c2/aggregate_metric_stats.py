import os
from datetime import datetime, timedelta

from google.cloud import monitoring_v3

def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int,
    reducer: monitoring_v3.Aggregation.Reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
    alignment_period_seconds: int = 300, # 5 minutes
):
    """Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={'seconds': int(end_time.timestamp())},
        start_time={'seconds': int(start_time.timestamp())},
    )

    query_filter = f'metric.type = "{metric_type}"'

    aggregation = monitoring_v3.Aggregation(
        alignment_period={'seconds': alignment_period_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_DELTA,
        cross_series_reducer=reducer,
        group_by_fields=['resource.label."instance_id"' if 'instance' in metric_type else 'resource.type'], # Example grouping
    )

    results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    return list(results)
