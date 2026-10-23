from datetime import datetime, timedelta
from typing import List, Dict, Optional

from observability_client import ObservabilityClient
from observability_models import MetricQueryResult, MetricDatapoint

def summarize_metric_trends(metric_name: str, namespace: str, duration_minutes: int, period_seconds: int, statistics: List[str], dimensions: Optional[Dict[str, str]] = None) -> str:
    client = ObservabilityClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)

    datapoints_raw = client.get_metric_data(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        statistics=statistics,
        dimensions=dimensions
    )

    if not datapoints_raw:
        return f"No data available for {metric_name} in namespace {namespace} over the last {duration_minutes} minutes."

    # Basic trend analysis: check if values are generally increasing or decreasing
    values = [dp.get(statistics[0]) for dp in datapoints_raw if dp.get(statistics[0]) is not None]

    if len(values) < 2:
        return f"Insufficient data points to determine a trend for {metric_name}. Current value: {values[0] if values else 'N/A'.}"

    first_value = values[0]
    last_value = values[-1]
    average_value = sum(values) / len(values)

    trend_description = "stable"
    if last_value > first_value * 1.1: # Increased by more than 10%
        trend_description = "increasing"
    elif last_value < first_value * 0.9: # Decreased by more than 10%
        trend_description = "decreasing"

    summary = f"Metric {metric_name} ({namespace}) over the last {duration_minutes} minutes:\n"
    summary += f"  - Average value: {average_value:.2f}\n"
    summary += f"  - Current trend: {trend_description} (from {first_value:.2f} to {last_value:.2f})\n"
    summary += f"  - Total datapoints: {len(values)}"

    return summary
