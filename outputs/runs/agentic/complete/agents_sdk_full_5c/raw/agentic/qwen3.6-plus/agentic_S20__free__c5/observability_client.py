"""Local configuration and client helper utilities for Managed Log Query / Log Ingestion.

Provider: Datadog Log Management API
- Log intake: https://http-intake.logs.datadoghq.com/api/v2/logs
- Log query API: https://api.datadoghq.com/api/v2/logs/events/search
- SDK: datadog-api-client
"""

import os
import json
import base64
from typing import Optional

# Datadog SDK import for API client management
try:
    from datadog_api_client import Configuration, ApiClient
    from datadog_api_client.v2.api.logs_api import LogsApi
    HAS_DATADOG_SDK = True
except ImportError:
    HAS_DATADOG_SDK = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


DATADOG_LOG_INTAKE_HOST = "https://http-intake.logs.datadoghq.com"
DATADOG_API_HOST = "https://api.datadoghq.com"
DATADOG_LOG_INTAKE_ENDPOINT = f"{DATADOG_LOG_INTAKE_HOST}/api/v2/logs"
DATADOG_LOG_SEARCH_ENDPOINT = f"{DATADOG_API_HOST}/api/v2/logs/events/search"


class DatadogObservabilityClient:
    """Helper client for Datadog Log Management operations.

    Uses either the official datadog-api-client SDK or falls back to
    direct HTTPS calls via requests for log ingestion and querying.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        app_key: Optional[str] = None,
        site: str = "datadoghq.com",
        use_sdk: bool = True,
    ):
        self.api_key = api_key or os.environ.get("DD_API_KEY", "")
        self.app_key = app_key or os.environ.get("DD_APP_KEY", "")
        self.site = site
        self.log_intake_host = f"https://http-intake.logs.{self.site}"
        self.api_host = f"https://api.{self.site}"
        self.use_sdk = use_sdk and HAS_DATADOG_SDK

        if self.use_sdk:
            self._config = Configuration()
            self._config.api_key["apiKeyAuth"] = self.api_key
            self._config.api_key["appKeyAuth"] = self.app_key
            self._config.host = self.api_host
            self._api_client = ApiClient(self._config)
            self._logs_api = LogsApi(self._api_client)

    def _headers(self) -> dict:
        """Build Datadog authentication headers for REST API calls."""
        return {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }

    def send_log_events(self, events: list[dict]) -> dict:
        """Send structured log events to Datadog HTTP Log Intake API.

        Reference: https://docs.datadoghq.com/api/latest/logs/#send-logs
        Endpoint: POST https://http-intake.logs.datadoghq.com/api/v2/logs
        """
        if self.use_sdk:
            return self._send_via_sdk(events)
        return self._send_via_http(events)

    def _send_via_sdk(self, events: list[dict]) -> dict:
        """Send logs using the datadog-api-client SDK."""
        body = {
            "data": [
                {
                    "type": "log",
                    "attributes": event,
                }
                for event in events
            ]
        }
        response = self._logs_api.submit_log(body=body)
        return {"status": "accepted", "raw": str(response)}

    def _send_via_http(self, events: list[dict]) -> dict:
        """Send logs via direct HTTP POST to Datadog log intake."""
        if not HAS_REQUESTS:
            raise RuntimeError("requests library required for HTTP fallback")
        url = f"{self.log_intake_host}/api/v2/logs"
        body = {
            "data": [
                {
                    "type": "log",
                    "attributes": event,
                }
                for event in events
            ]
        }
        resp = requests.post(url, headers=self._headers(), json=body, timeout=30)
        resp.raise_for_status()
        return {"status": resp.status_code, "body": resp.json()}

    def search_logs(self, body: dict) -> dict:
        """Search logs using the Datadog Logs API v2.

        Reference: https://docs.datadoghq.com/api/latest/logs/#search-logs
        Endpoint: POST https://api.datadoghq.com/api/v2/logs/events/search
        """
        if self.use_sdk:
            return self._search_via_sdk(body)
        return self._search_via_http(body)

    def _search_via_sdk(self, body: dict) -> dict:
        """Search logs using the datadog-api-client SDK."""
        response = self._logs_api.search_logs(body=body)
        return response.to_dict()

    def _search_via_http(self, body: dict) -> dict:
        """Search logs via direct HTTP POST to Datadog API."""
        if not HAS_REQUESTS:
            raise RuntimeError("requests library required for HTTP fallback")
        url = f"{self.api_host}/api/v2/logs/events/search"
        resp = requests.post(url, headers=self._headers(), json=body, timeout=30)
        resp.raise_for_status()
        return resp.json()


def get_observability_client() -> DatadogObservabilityClient:
    """Factory function to create a configured Datadog observability client."""
    return DatadogObservabilityClient(
        api_key=os.environ.get("DD_API_KEY"),
        app_key=os.environ.get("DD_APP_KEY"),
        site=os.environ.get("DD_SITE", "datadoghq.com"),
    )
