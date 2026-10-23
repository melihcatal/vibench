from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id


def get_aggregated_metrics(
    metric_type: str,
    minutes: int = 60,
    aligner: str = "ALIGN_MEAN",
    reducer: str = "REDUCE_MEAN",
    group_by_fields: list[str] = None,
) -> monitoring_v3.services.metric_service.pagers.ListTimeSeriesPager:

    client = get_monitoring_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 600},  # 10 minutes
            "per_series_aligner": getattr(monitoring_v3.Aggregation.Aligner, aligner),
            "cross_series_reducer": getattr(monitoring_v3.Aggregation.Reducer, reducer),
            "group_by_fields": group_by_fields or ["resource.zone"],
        }
    )

    request = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": aggregation,
    }

    results = client.list_time_series(request)
    return results
