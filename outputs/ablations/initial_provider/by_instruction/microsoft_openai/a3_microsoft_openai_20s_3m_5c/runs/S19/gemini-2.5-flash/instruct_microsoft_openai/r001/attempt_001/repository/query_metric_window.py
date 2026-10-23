import os
from datetime import datetime, timedelta
from typing import Optional, Dict

from observability_client import OpenAIMetricsClient
from observability_models import MetricQueryRequest, MetricQueryResponse

def query_metric_window(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    interval: Optional[str] = None,
    dimensions_filter: Optional[Dict[str, str]] = None
) -> MetricQueryResponse:
    """
    Queries recent datapoints for a named metric over a time window using OpenAI to simulate the response.

    Args:
        metric_name: The name of the metric to query.
        start_time: The start of the time window.
        end_time: The end of the time window.
        interval: The aggregation interval (e.g., 'PT1M' for 1 minute). Not used by OpenAI directly but passed in request.
        dimensions_filter: A dictionary of dimension names and values to filter the metrics.

    Returns:
        A MetricQueryResponse object containing the queried metric data.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAIMetricsClient(api_key=openai_api_key)
    
    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        interval=interval,
        dimensions_filter=dimensions_filter
    )
    
    response = client.query_metric_window(request)
    return response

if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY environment variable to be set)
    # For demonstration purposes, let's use a fixed time window.
    end_time_example = datetime.utcnow()
    start_time_example = end_time_example - timedelta(hours=1)

    print(f"Querying metric 'cpu_usage' from {start_time_example} to {end_time_example}")
    try:
        metric_data = query_metric_window(
            metric_name="cpu_usage",
            start_time=start_time_example,
            end_time=end_time_example,
            interval="PT1M",
            dimensions_filter={"host": "server1", "region": "us-east-1"}
        )

        print(f"\nMetric Name: {metric_data.metric_name}")
        print(f"Unit: {metric_data.unit}")
        print("Data Points:")
        for dp in metric_data.data_points:
            print(f"  Timestamp: {dp.timestamp}, Value: {dp.value}, Dimensions: {dp.dimensions}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

