import time
from datetime import datetime, timedelta, timezone
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.services.metric_service import MetricServiceClient
from observability_client import get_monitoring_client
from observability_models import AggregatedMetricStats


def get_aggregated_statistics(
    project_id: str, metric_type: str, window_minutes: int, aggregation_type: str
) -> list[AggregatedMetricStats]:
    client: MetricServiceClient = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    # Supported aggregations include ALIGN_MEAN, ALIGN_MAX, ALIGN_MIN, ALIGN_SUM, etc.
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": window_minutes * 60},
            "per_series_aligner": getattr(
                monitoring_v3.Aggregation.Aligner, aggregation_type
            ),
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_NONE,
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

    stats_list = []
    for result in results:
        for point in result.points:
            stats = AggregatedMetricStats(
                metric_name=result.metric.type,
                aggregation=aggregation_type,
                value=point.value.double_value,
                time_window={
                    "start": start_time.isoformat(),
                    "end": now.isoformat(),
                },
            )
            stats_list.append(stats)

    return stats_list
