import requests
from observability_client import get_aws_credentials, normalize_response
from observability_models import MetricStatResponse

# Example using Datadog Metrics API (could be swapped for other providers)


def summarize_metric_trends(metric_names, start_time, end_time, api_key, app_key):
    """Summarize recent metric trends or anomalies using Datadog Metrics API.

    Parameters:
        metric_names (list[str]): List of metric names to summarize.
        start_time (int): Unix timestamp (seconds) for the start of the window.
        end_time (int): Unix timestamp (seconds) for the end of the window.
        api_key (str): Datadog API key.
        app_key (str): Datadog application key.

    Returns:
        dict: Summary dict with high-level statistics per metric.
    """
    url = "https://api.datadoghq.com/api/v1/query"
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }
    payload = {
        "from": start_time,
        "to": end_time,
        "queries": metric_names,  # Datadog accepts list of query strings
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    # Normalize responses to a common shape
    summary = {}
    for query in data.get("series", []):
        metric = query["metric"]
        points = query.get("points", [])
        if points:
            avg = sum(p[1] for p in points) / len(points)
            summary[metric] = {
                "average": avg,
                "min": min(p[1] for p in points),
                "max": max(p[1] for p in points),
            }
    return summary
