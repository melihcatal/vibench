import os
import json
from ibm_watsonx_ai import WatsonxApi


class LogClient:
    """Helper wrapper for IBM Cloud Logs (IBM WatsonX) logging API."""

    _API_BASE = "https://logs.eu-de.logging.cloud.ibm.com"

    def __init__(self):
        self.api_key = os.getenv("IBM_CLOUD_API_KEY")
        self.instance_id = os.getenv("IBM_LOGS_INSTANCE_ID")
        self.client = WatsonxApi(base_url=self._API_BASE, api_key=self.api_key)

    def put_log_events(
        self, log_group_name: str, log_stream_name: str, log_events: list[dict]
    ) -> None:
        payload = {
            "logGroupName": log_group_name,
            "logStreamName": log_stream_name,
            "logEvents": log_events,
        }
        resp = self.client.post(f"/v1/logs", json=payload)
        resp.raise_for_status()

    def query(self, params) -> list[dict]:
        resp = self.client.post(f"/v1/query", json=params)
        resp.raise_for_status()
        return resp.json()

    def create_logs(self, logs: list[dict]) -> None:
        payload = {"logs": logs}
        resp = self.client.post(f"/v1/logs/ingest", json=payload)
        resp.raise_for_status()

    def list_log_entries(self, filter_expr: str, limit: int = 100) -> list[dict]:
        payload = {"filter": filter_expr, "limit": limit}
        resp = self.client.post(f"/v1/logs/search", json=payload)
        resp.raise_for_status()
        return resp.json()
