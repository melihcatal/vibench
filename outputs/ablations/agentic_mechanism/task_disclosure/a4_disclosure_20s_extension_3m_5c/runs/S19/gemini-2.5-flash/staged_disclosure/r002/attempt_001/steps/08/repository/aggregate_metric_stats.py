from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_response import MetricsQueryResponse
from datadog_api_client.v1.model.metric_query_resource_type import MetricQueryResourceType
import time
import os

def get_aggregated_metric_stats(metric_name: str, start_time: int, end_time: int, interval: int = 300) -> MetricsQueryResponse:
    """
    Retrieves aggregated statistics for a metric over a time window using Datadog.

    Args:
        metric_name: The name of the metric to query.
        start_time: The start of the time window in Unix timestamp format.
        end_time: The end of the time window in Unix timestamp format.
        interval: The aggregation interval in seconds.

    Returns:
        A MetricsQueryResponse object containing the aggregated metric data.
    """
    metrics_api = MetricsApi()

    # Ensure Datadog API key and Application key are set as environment variables
    # DD_API_KEY and DD_APP_KEY
    if not os.getenv("DD_API_KEY") or not os.getenv("DD_APP_KEY"):
        raise ValueError("Datadog API Key (DD_API_KEY) and Application Key (DD_APP_KEY) must be set as environment variables.")

    # Construct the query string
    # For simplicity, this example assumes a simple metric query.
    # More complex queries can be constructed as needed.
    query = f"avg:{metric_name}{{*}_by_host"

    response = metrics_api.query_metrics(
        _from=start_time,
        to=end_time,
        query=query,
        # Optional: You can specify an interval for aggregation
        # interval=interval
    )
    return response

if __name__ == "__main__":
    # Example usage (replace with your actual metric and time range)
    metric_to_query = "system.cpu.idle"
    
    # Get current time and 1 hour ago for demonstration
    end_ts = int(time.time())
    start_ts = end_ts - 3600  # 1 hour ago

    try:
        print(f"Fetching aggregated statistics for metric: {metric_to_query} from {start_ts} to {end_ts}")
        stats = get_aggregated_metric_stats(metric_to_query, start_ts, end_ts)
        print("Aggregated Metric Statistics:")
        for series in stats.series:
            print(f"  Metric: {series.metric}")
            print(f"  Scope: {series.scope}")
            print(f"  Display Name: {series.display_name}")
            print(f"  Pointlist: {series.pointlist}")
    except Exception as e:
        print(f"An error occurred: {e}")
