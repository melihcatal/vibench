import os
import json
from typing import Any, Dict


class ObservabilityClient:
    """Local helper client for Managed Log Query / Log Ingestion.
    Encapsulates configuration, authentication and request handling.
    """

    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv("DATADOG_API_KEY")
        self.base_url = base_url or "https://http-intake.logs.datadoghq.com/v1/input"
        self.headers = {"DD-API-KEY": self.api_key, "Content-Type": "application/json"}

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Any:
        """Internal POST helper."""
        import requests

        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def send_log(self, log: Dict[str, Any]) -> None:
        """Send a single structured log event."""
        self._post("", payload=log)

    def send_logs(self, logs: list[Dict[str, Any]]) -> None:
        """Send multiple logs in one request."""
        for log in logs:
            self.send_log(log)

    def query_logs(self, query: str, start: int, end: int) -> list[Dict[str, Any]]:
        """Query Datadog Logs API."""
        url = f"{self.base_url}/api/v1/logs/queries"
        payload = {"index": "default", "start": start, "end": end, "query": query}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("logs", [])


# Example usage (removed in final file)
# client = ObservabilityClient()
# client.send_log({"service": "my-app", "message": "Startup", "severity": "info"})
