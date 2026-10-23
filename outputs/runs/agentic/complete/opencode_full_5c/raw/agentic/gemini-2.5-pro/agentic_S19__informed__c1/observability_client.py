import os
import requests
from typing import Optional


class DatadogClient:
    def __init__(self, api_key: Optional[str] = None, app_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DD_API_KEY")
        self.app_key = app_key or os.getenv("DD_APP_KEY")
        if not self.api_key or not self.app_key:
            raise ValueError(
                "Datadog API key and App key must be provided or set as environment variables DD_API_KEY and DD_APP_KEY"
            )

        self.base_url = "https://api.datadoghq.com/api/v1"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "DD-API-KEY": self.api_key,
                "DD-APPLICATION-KEY": self.app_key,
            }
        )

    def query_metrics(self, query: str, from_ts: int, to_ts: int) -> dict:
        url = f"{self.base_url}/query"
        params = {
            "query": query,
            "from": from_ts,
            "to": to_ts,
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()


def get_datadog_client() -> DatadogClient:
    return DatadogClient()
