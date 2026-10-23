import requests
import os
from typing import List, Dict, Any, Optional

from observability_client import ClientFactory
from observability_models import MetricData, TimeSeriesPoint


def compare_dynatrace_metric_series(
    metric_selector_a: str,
    metric_selector_b: str,
    resolution: str = "1h",
    time_from: Optional[str] = "now-24h"
) -> Dict[str, List[MetricData]]:
    """
    Compares two metric series from Dynatrace over the same window.

    Args:
        metric_selector_a: The selector for the first metric series (e.g., "builtin:host.cpu.usage:filter(eq(\"dt.entity.host\", \"HOST-XYZ\"))").
        metric_selector_b: The selector for the second metric series.
        resolution: The time resolution for data points (e.g., "1h", "5m").
        time_from: The start of the time window (e.g., "now-24h").

    Returns:
        A dictionary containing the data for both series.
    """
    token = ClientFactory.get_dynatrace_api_token()
    env_id = ClientFactory.get_dynatrace_environment_id()

    if not token or not env_id:
        raise ValueError("Dynatrace API token and environment ID must be set.")
    
    base_url = f"https://{env_id}.live.dynatrace.com"
    endpoint = "/api/v2/metrics/query"
    
    headers = {
        "Authorization": f"Api-Token {token}",
        "Content-Type": "application/json",
    }
    
    params = {
        "metricSelector": f"({metric_selector_a}),({metric_selector_b})",
        "resolution": resolution,
        "from": time_from,
    }

    try:
        response = requests.get(f"{base_url}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        results = {"series_a": [], "series_b": []}
        
        for series in data.get("result", []):
            metric_id = series.get("metricId")
            points = [
                TimeSeriesPoint(timestamp=ts, value=val)
                for ts, val in zip(series.get("timestamps", []), series.get("values", []))
                if val is not None
            ]
            
            dimensions = {dim['key']: dim['value'] for dim in series.get('dimensions', [])}

            metric_data = MetricData(
                metric_name=metric_id,
                points=points,
                dimensions=dimensions,
            )

            # Heuristic to sort series A and B based on the original selector
            if metric_selector_a.split(":")[0] in metric_id:
                 results["series_a"].append(metric_data)
            elif metric_selector_b.split(":")[0] in metric_id:
                 results["series_b"].append(metric_data)
                 
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error calling Dynatrace API: {e}")
        if e.response:
            print(f"Response body: {e.response.text}")
        return {"series_a": [], "series_b": []}

# Example usage would require Dynatrace credentials.
# if __name__ == '__main__':
#     if os.environ.get("DYNATRACE_API_TOKEN") and os.environ.get("DYNATRACE_ENVIRONMENT_ID"):
#         # Replace with actual host IDs from your Dynatrace environment
#         host_a = "HOST-EXAMPLE-A"
#         host_b = "HOST-EXAMPLE-B"
#         selector_a = f'builtin:host.cpu.usage:filter(eq("dt.entity.host", "{host_a}")):splitBy("dt.entity.host")'
#         selector_b = f'builtin:host.cpu.usage:filter(eq("dt.entity.host", "{host_b}")):splitBy("dt.entity.host")'
#
#         comparison = compare_dynatrace_metric_series(selector_a, selector_b)
#
#         print("--- Series A ---")
#         for series in comparison["series_a"]:
#             print(f"Metric: {series.metric_name}, Dimensions: {series.dimensions}")
#             print(f"  Points: {len(series.points)}")
#
#         print("\n--- Series B ---")
#         for series in comparison["series_b"]:
#             print(f"Metric: {series.metric_name}, Dimensions: {series.dimensions}")
#             print(f"  Points: {len(series.points)}")
#     else:
#         print("DYNATRACE_API_TOKEN and DYNATRACE_ENVIRONMENT_ID must be set.")
