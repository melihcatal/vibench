from datetime import datetime, timedelta
from typing import Dict
from observability_client import ObservabilityClient
from observability_models import MetricSeries, MetricStats, MetricComparison
from query_metric_window import query_metric_window
from filter_metric_dimensions import filter_metric_dimensions


def compare_metric_series(
    metric_name: str, filter_a: Dict[str, str], filter_b: Dict[str, str], hours: int = 1
) -> MetricComparison:
    series_a = filter_metric_dimensions(metric_name, filter_a, hours)
    series_b = filter_metric_dimensions(metric_name, filter_b, hours)

    values_a = [p.value for p in series_a.points]
    values_b = [p.value for p in series_b.points]

    diffs = [a - b for a, b in zip(values_a, values_b)]

    return MetricComparison(
        series_a=series_a,
        series_b=series_b,
        diff_stats=MetricStats(
            count=len(diffs),
            mean=sum(diffs) / len(diffs) if diffs else 0.0,
            min=min(diffs) if diffs else 0.0,
            max=max(diffs) if diffs else 0.0,
            sum=sum(diffs),
        ),
    )
