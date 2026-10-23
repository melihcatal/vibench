# metric_summary.py
import os
from observability_client import ManagedMetricsClient
from observability_models import MetricQueryRequest, MetricQueryResponse

# Concrete provider: Alibaba CloudMonitor
# Required env vars: ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET

def summarize_recent_trends(metric_name: str, start: str, end: str, granularity: int = 300) -> str:
    """Summarize recent metric trends or simple anomalies using Alibaba CloudMonitor.
    
    Args:
        metric_name: CloudMonitor metric identifier (e.g., "acs_ecs_dashboard.TopCPUHosts").
        start: ISO8601 start timestamp.
        end: ISO8601 end timestamp.
        granularity: Data point interval in seconds for the summary.
    
    Returns:
        Human‑readable summary string.
    """
    client = ManagedMetricsClient()
    request = MetricQueryRequest(metric=metric_name, start=start, end=end)
    response: MetricQueryResponse = client.query_metrics(request)
    # Simple aggregation
    values = [point['value'] for point in response.series[0]['values']]
    avg = sum(values) / len(values)
    max_val = max(values)
    min_val = min(values)
    summary = (
        f"Metric {metric_name} over {start} → {end} (granularity {granularity}s):\n"
        f"Average = {avg:.2f}, Max = {max_val:.2f}, Min = {min_val:.2f}"
    )
    return summary

if __name__ == "__main__":
    # Example usage (ensure Alibaba credentials are set)
    print(summarize_recent_trends(
        metric_name="acs_ecs_dashboard.TopCPUHosts",
        start="2024-08-01T00:00:00Z",
        end="2024-08-02T00:00:00Z"
    ))
