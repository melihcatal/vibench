from datetime import datetime, timedelta, timezone
from typing import List, Optional

from observability_client import ObservabilityClient
from observability_models import (
    MetricAggregationResult,
    MetricDimension,
    MetricStatistic,
    normalize_period_to_seconds,
    parse_dimension_string,
)

CLOUDWATCH_NAMESPACE = "AWS/EC2"
DEFAULT_METRIC_NAME = "CPUUtilization"
DEFAULT_PERIOD_MINUTES = 5


def aggregate_metric_stats(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    dimensions: Optional[List[MetricDimension]] = None,
    region: Optional[str] = None,
) -> MetricAggregationResult:
    period_seconds = normalize_period_to_seconds(period_minutes)

    client = ObservabilityClient(region=region)

    result = client.get_metric_aggregation(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        dimensions=dimensions,
    )

    return result


def aggregate_metric_stats_by_string(
    namespace: str = CLOUDWATCH_NAMESPACE,
    metric_name: str = DEFAULT_METRIC_NAME,
    window_minutes: int = 60,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    dimensions_str: str = "",
    region: Optional[str] = None,
) -> MetricAggregationResult:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=window_minutes)

    dimensions = parse_dimension_string(dimensions_str)

    return aggregate_metric_stats(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period_minutes=period_minutes,
        dimensions=dimensions,
        region=region,
    )


def format_aggregation_results(result: MetricAggregationResult) -> str:
    lines = [
        f"Aggregation: {result.namespace}/{result.metric_name}",
        f"Window: {result.start_time.strftime('%Y-%m-%d %H:%M:%S')} to {result.end_time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Period: {result.period}s",
        f"Datapoints analyzed: {result.datapoint_count}",
        "",
        "Statistics:",
    ]

    for stat, value in result.statistics.items():
        lines.append(f"  {stat.value}: {value:.4f}")

    return "\n".join(lines)
