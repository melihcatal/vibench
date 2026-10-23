import os
from typing import Dict, List, Optional
from datetime import datetime

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


class DatadogLoggingClient:
    """
    A client for interacting with Datadog's log ingestion and query APIs.
    """

    def __init__(self):
        configuration = Configuration()
        configuration.api_key["apiKeyAuth"] = os.getenv("DD_API_KEY")
        configuration.api_key["appKeyAuth"] = os.getenv("DD_APP_KEY")
        self.api_client = ApiClient(configuration)
        self.logs_api = LogsApi(self.api_client)

    def send(self, log_entry: Dict) -> None:
        """
        Sends a log entry to Datadog's HTTP log intake.

        Args:
            log_entry: A dictionary representing the log entry.
        """
        body = HTTPLog(
            [
                HTTPLogItem(
                    message=log_entry.get("message", ""),
                    ddsource=log_entry.get("ddsource", "python"),
                    ddtags=log_entry.get("ddtags", ""),
                    hostname=log_entry.get("host", "localhost"),
                    service=log_entry.get("service", "default-service"),
                    status=log_entry.get("status", "INFO"),
                    timestamp=log_entry.get(
                        "timestamp", datetime.utcnow().isoformat() + "Z"
                    ),
                    **{
                        k: v
                        for k, v in log_entry.items()
                        if k
                        not in [
                            "message",
                            "ddsource",
                            "ddtags",
                            "host",
                            "service",
                            "status",
                            "timestamp",
                        ]
                    },
                )
            ]
        )
        self.logs_api.submit_log(body=body)

    def query(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime,
        limit: int = 100,
    ) -> List[Dict]:
        """
        Queries logs from Datadog using the Logs API.

        Args:
            query: The query string to filter logs.
            start_time: The start time for the query.
            end_time: The end time for the query.
            limit: Maximum number of logs to return.

        Returns:
            A list of log entries matching the query.
        """
        response = self.logs_api.list_logs(
            body={
                "filter": {
                    "from": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "to": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "query": query,
                },
                "page": {"limit": limit},
            }
        )

        logs = []
        for log in response.data:
            log_dict = {
                "id": log.id,
                "message": log.attributes.message,
                "status": log.attributes.status,
                "timestamp": log.attributes.timestamp,
                "service": log.attributes.service,
                **log.attributes.attributes,
            }
            logs.append(log_dict)

        return logs


def get_logging_client() -> DatadogLoggingClient:
    """
    Returns a configured instance of the Datadog logging client.
    """
    return DatadogLoggingClient()
