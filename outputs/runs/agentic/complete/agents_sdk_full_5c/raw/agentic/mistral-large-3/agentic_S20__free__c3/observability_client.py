import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


def get_logging_client():
    """Initialize and return a Datadog logs client."""
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = os.getenv("DD_API_KEY")
    configuration.api_key["appKeyAuth"] = os.getenv("DD_APP_KEY")
    
    with ApiClient(configuration) as api_client:
        return LogsApi(api_client)


class DatadogLogsClient:
    """Wrapper for Datadog logs API operations."""
    
    def __init__(self, client):
        self.client = client
    
    def submit_log(self, body: dict, content_encoding: str = "application/json") -> dict:
        """Submit a single log to Datadog."""
        log_item = HTTPLogItem(
            ddsource="python",
            ddtags="env:prod",
            hostname="app-server",
            message=body.get("message", ""),
            service="log-integration-service",
            status=body.get("severity", "INFO"),
            attributes=body.get("attributes", {})
        )
        
        response = self.client.submit_log(
            content_encoding=content_encoding,
            body=HTTPLog([log_item])
        )
        return {"log_id": response.get("status")}
    
    def submit_logs(self, logs: list) -> list:
        """Submit multiple logs to Datadog."""
        log_items = []
        for log in logs:
            log_items.append(HTTPLogItem(
                ddsource="python",
                ddtags="env:prod",
                hostname="app-server",
                message=log.get("message", ""),
                service="log-integration-service",
                status=log.get("severity", "INFO"),
                attributes=log.get("attributes", {})
            ))
        
        response = self.client.submit_log(
            content_encoding="application/json",
            body=HTTPLog(log_items)
        )
        return [{"log_id": resp} for resp in response.get("status", [])]
    
    def query_logs(self, query: str, time_range: tuple) -> dict:
        """Query logs from Datadog."""
        response = self.client.list_logs(
            filter_query=query,
            filter_from=str(time_range[0]),
            filter_to=str(time_range[1]),
            page_limit=1000
        )
        return {"logs": [log.to_dict() for log in response.data] if response.data else []}