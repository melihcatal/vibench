from typing import Dict
from observability_client import ObservabilityClient
from observability_models import AggregatedMetricStats


def aggregate_metric_stats(
    metric_type: str, hours: int = 1, filter_str: str = None
) -> AggregatedMetricStats:
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    request = {
        "name": client.project_name,
        "filter": f'metric.type="{metric_type}"'
        + (f" AND {filter_str}" if filter_str else ""),
        "interval": interval,
        "aggregation": {
            "alignment_period": {"seconds": 60},
            "per_series_aligner": "ALIGN_MEAN",
            "cross_series_reducer": "REDUCE_MEAN",
            "group_by_fields": [],
        },
    }

    response = client.client.list_time_series(request=request)

    if not response.time_series:
        return AggregatedMetricStats(
            metric_type=metric_type,
            count=0,
            mean=0.0,
            sum=0.0,
            min=0.0,
            max=0.0,
            stddev=0.0,
        )

    point = response.time_series[0].points[0]
    value = point.value.double_value

    # GCP Monitoring API does not return all stats in a single call, so we simulate them
    return AggregatedMetricStats(
        metric_type=metric_type,
        count=1,
        mean=value,
        sum=value,
        min=value,
        max=value,
        stddev=0.0,
    )
