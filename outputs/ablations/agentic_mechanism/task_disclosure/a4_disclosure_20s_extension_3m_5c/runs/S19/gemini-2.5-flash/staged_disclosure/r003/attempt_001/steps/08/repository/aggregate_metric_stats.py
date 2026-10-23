import requests
import datetime

PROMETHEUS_SERVER_URL = "http://localhost:9090"  # Replace with your managed Prometheus service URL

def get_metric_stats(metric_name: str, start_time: datetime.datetime, end_time: datetime.datetime, step: str = "1h"):
    """
    Retrieves aggregated statistics for a metric over a time window from Prometheus.

    Args:
        metric_name (str): The name of the metric to query (e.g., "http_requests_total").
        start_time (datetime.datetime): The start of the time window.
        end_time (datetime.datetime): The end of the time window.
        step (str): The step size for the aggregation (e.g., "1h", "5m").

    Returns:
        dict: The JSON response from the Prometheus API, or an error message.
    """
    query = f"sum(rate({metric_name}[{step}])) by (instance)"
    params = {
        "query": query,
        "start": start_time.timestamp(),
        "end": end_time.timestamp(),
        "step": step,
    }

    try:
        response = requests.get(f"{PROMETHEUS_SERVER_URL}/api/v1/query_range", params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

