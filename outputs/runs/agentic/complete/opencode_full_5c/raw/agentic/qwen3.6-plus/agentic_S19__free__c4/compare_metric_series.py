from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from observability_client import ObservabilityClient
from observability_models import (
    MetricComparisonResult,
    MetricDataPoint,
    MetricDimension,
    MetricStatistic,
    normalize_period_to_seconds,
    parse_dimension_string,
)

CLOUDWATCH_NAMESPACE = "AWS/EC2"
DEFAULT_METRIC_NAME = "CPUUtilization"
DEFAULT_PERIOD_MINUTES = 5


def compare_metric_series(
    namespace: str,
    metric_name: str,
    series_a_dimensions: List[MetricDimension],
    series_b_dimensions: List[MetricDimension],
    start_time: datetime,
    end_time: datetime,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    statistic: MetricStatistic = MetricStatistic.AVERAGE,
    region: Optional[str] = None,
) -> MetricComparisonResult:
    period_seconds = normalize_period_to_seconds(period_minutes)

    client = ObservabilityClient(region=region)

    response_a = client.get_metric_data(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        dimensions=series_a_dimensions,
        statistics=[statistic],
    )

    response_b = client.get_metric_data(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        dimensions=series_b_dimensions,
        statistics=[statistic],
    )

    datapoints_a = response_a.datapoints
    datapoints_b = response_b.datapoints

    aligned_a, aligned_b = _align_datapoints(datapoints_a, datapoints_b)

    delta_values = []
    delta_percentage = []

    for dp_a, dp_b in zip(aligned_a, aligned_b):
        delta = dp_b.value - dp_a.value
        delta_values.append(delta)
        if dp_a.value != 0:
            delta_percentage.append((delta / dp_a.value) * 100.0)
        else:
            delta_percentage.append(0.0)

    label_a = ",".join(f"{d.name}={d.value}" for d in series_a_dimensions) or "series_a"
    label_b = ",".join(f"{d.name}={d.value}" for d in series_b_dimensions) or "series_b"

    return MetricComparisonResult(
        series_a_label=label_a,
        series_b_label=label_b,
        series_a_datapoints=aligned_a,
        series_b_datapoints=aligned_b,
        delta_values=delta_values,
        delta_percentage=delta_percentage,
    )


def compare_metric_series_by_string(
    namespace: str = CLOUDWATCH_NAMESPACE,
    metric_name: str = DEFAULT_METRIC_NAME,
    series_a_dimensions_str: str = "",
    series_b_dimensions_str: str = "",
    window_minutes: int = 60,
    period_minutes: int = DEFAULT_PERIOD_MINUTES,
    statistic: str = "Average",
    region: Optional[str] = None,
) -> MetricComparisonResult:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=window_minutes)

    dimensions_a = parse_dimension_string(series_a_dimensions_str)
    dimensions_b = parse_dimension_string(series_b_dimensions_str)

    stat_enum = MetricStatistic(statistic)

    return compare_metric_series(
        namespace=namespace,
        metric_name=metric_name,
        series_a_dimensions=dimensions_a,
        series_b_dimensions=dimensions_b,
        start_time=start_time,
        end_time=end_time,
        period_minutes=period_minutes,
        statistic=stat_enum,
        region=region,
    )


def _align_datapoints(
    datapoints_a: List[MetricDataPoint],
    datapoints_b: List[MetricDataPoint],
) -> tuple:
    timestamps_a = {dp.timestamp: dp for dp in datapoints_a}
    timestamps_b = {dp.timestamp: dp for dp in datapoints_b}

    common_timestamps = sorted(set(timestamps_a.keys()) & set(timestamps_b.keys()))

    aligned_a = [timestamps_a[ts] for ts in common_timestamps]
    aligned_b = [timestamps_b[ts] for ts in common_timestamps]

    return aligned_a, aligned_b


def format_comparison_results(result: MetricComparisonResult) -> str:
    lines = [
        f"Comparison: {result.series_a_label} vs {result.series_b_label}",
        f"Aligned datapoints: {len(result.series_a_datapoints)}",
        "",
    ]

    for i, (dp_a, dp_b) in enumerate(
        zip(result.series_a_datapoints, result.series_b_datapoints)
    ):
        ts = dp_a.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
        delta = result.delta_values[i]
        delta_pct = result.delta_percentage[i]
        lines.append(
            f"  {ts} | A={dp_a.value:.4f} B={dp_b.value:.4f} "
            f"delta={delta:+.4f} ({delta_pct:+.2f}%)"
        )

    return "\n".join(lines)
