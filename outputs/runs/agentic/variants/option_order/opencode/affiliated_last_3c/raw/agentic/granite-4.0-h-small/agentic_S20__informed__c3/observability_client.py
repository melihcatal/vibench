import logging
import os
from pathlib import Path


class ManagedLogClient:
    """Local configuration and client helper utilities for Managed Log Query / Log Ingestion.",
    "+Methods: rest_call, put_log_events, submit_log, query_logs, get_environment"""

    def __init__(self):
        # Detect service based on environment variables (provider-specific)
        if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
            self.service = "aws-cloudwatch"
            from boto3 import client as boto_client

            self.log_client = boto_client("logs")
        elif (
            os.getenv("AZURE_TENANT_ID")
            and os.getenv("AZURE_CLIENT_ID")
            and os.getenv("AZURE_CLIENT_SECRET")
        ):
            self.service = "azure-monitor"
            # Placeholder for azure sdk initialization (could use azure-identity + azure-monitor)
            pass
        elif os.getenv("DD_API_KEY") and os.getenv("DD_APP_KEY"):
            self.service = "datadog"
            # Placeholder for datadog API client initialization
            pass
        elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self.service = "gcp-logging"
            # Placeholder for google-cloud-logging initialization
            pass
        else:
            raise RuntimeError(
                "No supported logging provider credentials found in environment"
            )

    def rest_call(self, method: str, url: str, json: dict = None, **kwargs) -> dict:
        """Generic REST call using the configured provider client.",
        "+Uses requests library for non-aws services."""
        import requests

        headers = kwargs.pop("headers", {})
        headers["Content-Type"] = "application/json"
        response = requests.request(method, url, json=json, headers=headers, **kwargs)
        return response.json()

    def put_log_events(self, log_group: str, log_stream: str, log_events: list) -> dict:
        """Push a batch of log events (AWS CloudWatch Logs)."""
        if self.service != "aws-cloudwatch":
            raise NotImplementedError(
                f"put_log_events not supported for {self.service}"
            )
        response = self.log_client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=log_events,
        )
        return {"status": "ok"}

    def submit_log(self, log_body: str, tags: list = None) -> dict:
        """Submit a single log entry (Datadog)."""
        if self.service != "datadog":
            raise NotImplementedError(f"submit_log not supported for {self.service}")
        # Use Datadog API endpoint "/v1/input"
        url = f"https://http-intake.logs.datadoghq.com/v1/input"
        payload = {
            "api_key": os.getenv("DD_API_KEY"),
            "application_key": os.getenv("DD_APP_KEY"),
            "ddsource": "app",
            "tags": tags or [],
            "logs": [json.loads(log_body)],
        }
        response = self.rest_call("POST", url, json=payload)
        return {"status": "ok"}

    def query_logs(self, query: str) -> list:
        """Query logs using Google Cloud Logging SDK interface.",
        "+Uses google.cloud.logging for GCP service."""
        if self.service != "gcp-logging":
            raise NotImplementedError(f"query_logs not supported for {self.service}")
        # Example stub – real implementation would use google.cloud.logging.Client
        return []

    def get_environment(self) -> dict:
        """Return a dict of the detected provider and its credential variables."""
        env = {"service": self.service}
        if self.service == "aws-cloudwatch":
            env.update(
                {
                    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
                    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
                }
            )
        elif self.service == "azure-monitor":
            env.update(
                {
                    "AZURE_TENANT_ID": os.getenv("AZURE_TENANT_ID"),
                    "AZURE_CLIENT_ID": os.getenv("AZURE_CLIENT_ID"),
                    "AZURE_CLIENT_SECRET": os.getenv("AZURE_CLIENT_SECRET"),
                }
            )
        elif self.service == "datadog":
            env.update(
                {
                    "DD_API_KEY": os.getenv("DD_API_KEY"),
                    "DD_APP_KEY": os.getenv("DD_APP_KEY"),
                }
            )
        elif self.service == "gcp-logging":
            env.update(
                {
                    "GOOGLE_APPLICATION_CREDENTIALS": os.getenv(
                        "GOOGLE_APPLICATION_CREDENTIALS"
                    )
                }
            )
        return env
