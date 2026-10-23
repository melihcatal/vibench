import os
import requests
from typing import Optional


class DatadogLoggingClient:
    """Client for Datadog log ingestion and query APIs."""

    def __init__(self):
        self.logs_intake_url = "https://http-intake.logs.datadoghq.com/api/v2/logs"
        self.logs_query_url = "https://api.datadoghq.com/api/v1/logs-queries/list"
        self.api_key = os.getenv("DD_API_KEY")
        self.app_key = os.getenv("DD_APP_KEY")

    def submit_log(self, body: str, headers: dict):
        """Submit a log to Datadog."""
        response = requests.post(self.logs_intake_url, data=body, headers=headers)
        response.raise_for_status()
        return response

    def query_logs(self, query: str, time_start: int, time_end: int, limit: int = 1000):
        """Query logs from Datadog."""
        headers = {
            "Content-Type": "application/json",
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
        }
        payload = {
            "query": query,
            "time": {"from": time_start, "to": time_end},
            "limit": limit,
        }
        response = requests.post(self.logs_query_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()


def get_logging_client():
    """Factory for Datadog logging client."""
    return DatadogLoggingClient()
