import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi

class DatadogLoggingClient:
    def __init__(self):
        configuration = Configuration()
        configuration.api_key["apiKeyAuth"] = os.getenv("DD_API_KEY")
        configuration.api_key["appKeyAuth"] = os.getenv("DD_APP_KEY")
        self.client = ApiClient(configuration)
        self.api = LogsApi(self.client)

    def submit_log(self, body: list, content_encoding: str = "json") -> dict:
        """Submit logs to Datadog."""
        response = self.api.submit_log(
            content_encoding=content_encoding,
            body=body
        )
        return {"status": response.status}

    def query_logs(self, query: str, time: dict) -> dict:
        """Query logs from Datadog."""
        response = self.api.list_logs(
            body={
                "query": query,
                "time": time,
                "page": {"limit": 1000}
            }
        )
        return {"logs": response.data}

def get_logging_client() -> DatadogLoggingClient:
    """Factory for Datadog logging client."""
    return DatadogLoggingClient()