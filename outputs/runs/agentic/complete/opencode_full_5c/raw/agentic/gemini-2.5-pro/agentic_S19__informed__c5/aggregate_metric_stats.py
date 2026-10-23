from datetime import datetime, timedelta, timezone
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id


def get_aggregated_metric_stats(
    project_id: str,
    metric_type: str,
    minutes_ago: int,
    aggregation_alignment_period_seconds: int = 300,
    per_series_aligner: str = "ALIGN_MEAN",
    cross_series_reducer: str = "REDUCE_SUM",
) -> list:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(now.timestamp())},
        }
    )

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": aggregation_alignment_period_seconds},
            "per_series_aligner": getattr(
                monitoring_v3.Aggregation.Aligner, per_series_aligner
            ),
            "cross_series_reducer": getattr(
                monitoring_v3.Aggregation.Reducer, cross_series_reducer
            ),
            "group_by_fields": ["metric.label.instance_name"],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    stats = []
    for result in results:
        stat_point = {
            "metric_labels": dict(result.metric.labels),
            "resource_labels": dict(result.resource.labels),
            "points": [
                {
                    "timestamp": p.interval.end_time.rfc3339(),
                    "value": p.value.double_value,
                }
                for p in result.points
            ],
        }
        stats.append(stat_point)

    return stats


if __name__ == "__main__":
    project = get_project_id()
    # Example: GCE CPU utilization, 5-minute mean, summed across instances
    metric = "compute.googleapis.com/instance/cpu/utilization"
    aggregated_data = get_aggregated_metric_stats(project, metric, 60)
    for data in aggregated_data:
        print(data)
