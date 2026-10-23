import time
from datetime import timedelta
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricQuery, AggregatedMetricStats


def aggregate_metric_stats(
    query: MetricQuery, aggregation_type: str = "ALIGN_MEAN"
) -> list[AggregatedMetricStats]:
    client, project_name = get_monitoring_client()

    now = time.time()
    start_time = now - timedelta(minutes=query.minutes_ago).total_seconds()
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now)},
            "start_time": {"seconds": int(start_time)},
        }
    )

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": query.minutes_ago * 60},
            "per_series_aligner": getattr(
                monitoring_v3.Aggregation.Aligner, aggregation_type
            ),
        }
    )

    filter_str = f'metric.type = "{query.metric_name}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    stats_list = []
    for result in results:
        if result.points:
            point = result.points[0]
            stats_list.append(
                AggregatedMetricStats(
                    metric_name=result.metric.type,
                    aggregation=aggregation_type,
                    value=point.value.double_value,
                    interval_seconds=query.minutes_ago * 60,
                    dimensions=dict(result.metric.labels),
                )
            )
    return stats_list
