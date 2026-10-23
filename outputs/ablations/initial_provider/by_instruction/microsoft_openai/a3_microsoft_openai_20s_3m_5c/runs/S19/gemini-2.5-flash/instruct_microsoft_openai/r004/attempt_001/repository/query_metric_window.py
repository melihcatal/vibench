import os
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import MetricWindowResponse

def query_recent_datapoints(
    metric_name: str,
    start_time: datetime,
    end_time: datetime
) -> MetricWindowResponse:
    """
    Queries recent datapoints for a named metric over a time window using OpenAI to simulate the response.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = ObservabilityClient(openai_api_key=openai_api_key)
    metric_window_response = client.query_openai_metric_window(metric_name, start_time, end_time)
    return metric_window_response
