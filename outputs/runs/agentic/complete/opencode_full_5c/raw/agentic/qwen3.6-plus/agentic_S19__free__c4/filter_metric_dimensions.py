from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from observability_client import ObservabilityClient
from observability_models import (
    MetricDataPoint,
    MetricDimension,
    MetricQueryResponse,
    MetricStatistic,
    normalize_period_to_seconds,
    parse_dimension_string,
)

CLOUDWATCH_NAMESPACE = "AWS/EC2"
DEFAULT_METRIC_NAME = "CPUUtilization"
DEFAULT_PERIOD_MINUTES = 5


def filter_metric_dimensions(
    namespace: str,
    metric_name: str,
    dimension_filters: Dict[str, str],
    start_time: datetime,
    end_time: datetime,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    statistic: MetricStatistic = MetricStatistic.AVERAGE,
    region: Optional[str] = None,
) -> List[MetricQueryResponse]:
    period_seconds = normalize_period_to_seconds(period_minutes)

    client = ObservabilityClient(region=region)

    dimensions = [
        MetricDimension(name=name, value=value)
        for name, value in dimension_filters.items()
    ]

    response = client.get_metric_data(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        dimensions=dimensions,
        statistics=[statistic],
    )

    return [response]


def filter_metric_dimensions_by_string(
    namespace: str = CLOUDWATCH_NAMESPACE,
    metric_name: str = DEFAULT_METRIC_NAME,
    dimensions_str: str = "",
    window_minutes: int = 60,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    statistic: str = "Average",
    region: Optional[str] = None,
) -> List[MetricQueryResponse]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=window_minutes)

    dimensions = parse_dimension_string(dimensions_str)
    dimension_filters = {d.name: d.value for d in dimensions}

    stat_enum = MetricStatistic(statistic)

    return filter_metric_dimensions(
        namespace=namespace,
        metric_name=metric_name,
        dimension_filters=dimension_filters,
        start_time=start_time,
        end_time=end_time,
        period_minutes=period_minutes,
        statistic=stat_enum,
        region=region,
    )


def filter_multiple_dimension_sets(
    namespace: str,
    metric_name: str,
    dimension_sets: List[Dict[str, str]],
    start_time: datetime,
    end_time: datetime,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    statistic: MetricStatistic = MetricStatistic.AVERAGE,
    region: Optional[str] = None,
) -> List[MetricQueryResponse]:
    results = []
    for dim_filters in dimension_sets:
        response = filter_metric_dimensions(
            namespace=namespace,
            metric_name=metric_name,
            dimension_filters=dim_filters,
            start_time=start_time,
            end_time=end_time,
            period_minutes=period_minutes,
            statistic=statistic,
            region=region,
        )
        results.extend(response)
    return results


def format_filtered_results(responses: List[MetricQueryResponse]) -> str:
    lines = []
    for response in responses:
        dim_str = (
            ", ".join(f"{d.name}={d.value}" for d in response.dimensions) or "none"
        )
        lines.append(f"Filter [{dim_str}]: {len(response.datapoints)} datapoints")
        for dp in response.datapoints:
            ts = dp.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
            lines.append(f"  {ts} | {dp.value:.4f} {dp.unit}")
        lines.append("")
    return "\n".join(lines)
