from observability_client import ObservabilityClient
from observability_models import MetricDatapoint, MetricComparisonResult
import datetime
from typing import List

# Provider identifying signal: datadog_api_client (intended import and client)

def compare_metric_series(
    metric_name: str,
    query_a: str, # Datadog metric query string for series A
    query_b: str, # Datadog metric query string for series B
    start_time: datetime.datetime,
    end_time: datetime.datetime,
) -> MetricComparisonResult:
    """Compares metric values for two resources or dimension filters over the same window using Datadog (simulated).

    Args:
        metric_name: The name of the metric being compared.
        query_a: The Datadog query string for the first metric series.
        query_b: The Datadog query string for the second metric series.
        start_time: The start of the time window.
        end_time: The end of the time window.

    Returns:
        A MetricComparisonResult containing simulated series data and a comparison summary.
    """
    datadog_client = ObservabilityClient().get_datadog_client()

    print(f"Simulating Datadog comparison for metric {metric_name} "
          f"between query A: '{query_a}' and query B: '{query_b}' "
          f"from {start_time} to {end_time}")

    # In a real scenario, you would use datadog_client.query_metrics(
    # from_=int(start_time.timestamp()), to=int(end_time.timestamp()), query=query_a)
    # and similar for query_b.

    # Simulate two series for comparison
    simulated_series_a: List[MetricDatapoint] = []
    simulated_series_b: List[MetricDatapoint] = []
    current_time = start_time
    time_delta = (end_time - start_time) / 4
    for i in range(5):
        timestamp = (current_time + i * time_delta).isoformat()
        simulated_series_a.append(MetricDatapoint(timestamp=timestamp, value=float(100 + (i * 5))))
        simulated_series_b.append(MetricDatapoint(timestamp=timestamp, value=float(90 + (i * 6))))

    comparison_summary = "Simulated comparison: Series B shows a slightly steeper upward trend than Series A."

    return MetricComparisonResult(
        metric_name=metric_name,
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
        series_a=simulated_series_a,
        series_b=simulated_series_b,
        comparison_summary=comparison_summary
    )
