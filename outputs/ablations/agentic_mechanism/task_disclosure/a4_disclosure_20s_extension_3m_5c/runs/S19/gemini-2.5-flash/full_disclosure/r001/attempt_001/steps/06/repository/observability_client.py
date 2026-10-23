import os
import requests

class ManagedMetricsClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_metric_data(self, metric_name: str, start_time: str, end_time: str):
        """
        Retrieves metric data from the managed metrics monitoring service.
        """
        endpoint = f"{self.base_url}/metrics/{metric_name}/data"
        params = {
            "startTime": start_time,
            "endTime": end_time
        }
        response = requests.get(endpoint, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

def get_observability_client():
    """
    Provides a configured client for Managed Metrics Monitoring.
    """
    api_key = os.environ.get("METRICS_API_KEY")
    base_url = os.environ.get("METRICS_BASE_URL", "https://api.examplemetrics.com/v1") # Example URL, replace with actual provider URL

    if not api_key:
        raise ValueError("METRICS_API_KEY environment variable not set.")

    return ManagedMetricsClient(api_key, base_url)
