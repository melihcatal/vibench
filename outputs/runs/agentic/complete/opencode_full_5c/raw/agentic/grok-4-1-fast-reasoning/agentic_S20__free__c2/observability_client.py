import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.models.logs_list_request import LogsListRequest
from datadog_api_client.v2.models.logs_list_request_time import LogsListRequestTime
from datadog_api_client.v2.models.logs_list_request_page import LogsListRequestPage


class ObservabilityClient:
    def __init__(self):
        self.site = os.getenv("DD_SITE", "datadoghq.com")
        self.api_key = os.getenv("DD_API_KEY")
        self.app_key = os.getenv("DD_APPLICATION_KEY")
        if not self.api_key or not self.app_key:
            raise ValueError("DD_API_KEY and DD_APPLICATION_KEY must be set")

    def submit_logs(self, logs: List[Dict[str, Any]]) -> requests.Response:
        url = f"https://http-intake.logs.{self.site}/api/v2/logs"
        headers = {
            "DD-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, json=logs)
        response.raise_for_status()
        return response

    def query_logs(
        self, query: str, from_timestamp: int, to_timestamp: int, limit: int = 10
    ) -> List[Dict[str, Any]]:
        configuration = Configuration()
        configuration.api_key["apiKeyAuth"] = self.api_key
        configuration.api_key["appKeyAuth"] = self.app_key
        api_client = ApiClient(configuration)
        api_instance = LogsApi(api_client)
        body = LogsListRequest(
            query=query,
            time=LogsListRequestTime(from_=from_timestamp, to=to_timestamp),
            page=LogsListRequestPage(limit=limit),
        )
        response = api_instance.list_logs(body=body)
        return [log.to_dict() for log in response.data] if response.data else []
