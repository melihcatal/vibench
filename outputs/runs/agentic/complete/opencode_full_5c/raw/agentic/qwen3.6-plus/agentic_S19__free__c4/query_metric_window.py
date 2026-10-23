from datetime import datetime, timedelta, timezone
from typing import List, Optional

from observability_client import ObservabilityClient
from observability_models import (
    MetricDataPoint,
    MetricDimension,
    MetricQueryResponse,
    MetricStatistic,
    MetricUnit,
    normalize_period_to_seconds,
    parse_dimension_string,
)

CLOUDWATCH_NAMESPACE = "AWS/EC2"
DEFAULT_METRIC_NAME = "CPUUtilization"
DEFAULT_PERIOD_MINUTES = 5


def query_metric_window(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    dimensions: Optional[List[MetricDimension]] = None,
    statistic: MetricStatistic = MetricStatistic.AVERAGE,
    unit: Optional[MetricUnit] = None,
    region: Optional[str] = None,
) -> MetricQueryResponse:
    period_seconds = normalize_period_to_seconds(period_minutes)

    client = ObservabilityClient(region=region)

    response = client.get_metric_data(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        dimensions=dimensions,
        statistics=[statistic],
        unit=unit.value if unit else None,
    )

    return response


def query_metric_window_by_string(
    namespace: str = CLOUDWATCH_NAMESPACE,
    metric_name: str = DEFAULT_METRIC_NAME,
    window_minutes: int = 60,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    dimensions_str: str = "",
    statistic: str = "Average",
    region: Optional[str] = None,
) -> MetricQueryResponse:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=window_minutes)

    dimensions = parse_dimension_string(dimensions_str)

    stat_enum = MetricStatistic(statistic)

    return query_metric_window(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period_minutes=period_minutes,
        dimensions=dimensions,
        statistic=stat_enum,
        region=region,
    )


def format_query_results(response: MetricQueryResponse) -> str:
    lines = [
        f"Metric: {response.namespace}/{response.metric_name}",
        f"Label: {response.label}",
        f"Dimensions: {', '.join(f'{d.name}={d.value}' for d in response.dimensions) or 'none'}",
        f"Datapoints: {len(response.datapoints)}",
        "",
    ]

    for dp in response.datapoints:
        ts = dp.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
        lines.append(f"  {ts} | {dp.value:.4f} {dp.unit}")

    return "\n".join(lines)
