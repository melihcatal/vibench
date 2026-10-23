import os
from typing import Optional, Dict, Any
import requests
from google.cloud import logging as google_logging
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential


class ObservabilityClient:
    """Client helper for interacting with managed logging services."""

    def __init__(self):
        self._datadog_client = None
        self._google_client = None
        self._azure_client = None
        self._aws_client = None

    def _get_datadog_client(self):
        if not self._datadog_client:
            self._datadog_client = requests.Session()
        return self._datadog_client

    def _get_google_client(self):
        if not self._google_client:
            self._google_client = google_logging.Client()
        return self._google_client

    def _get_azure_client(self):
        if not self._azure_client:
            credential = DefaultAzureCredential()
            self._azure_client = LogsQueryClient(credential)
        return self._azure_client

    def _get_aws_client(self):
        if not self._aws_client:
            import boto3

            self._aws_client = boto3.client("logs")
        return self._aws_client


def get_logging_client(service: Optional[str] = None) -> ObservabilityClient:
    """Factory method to get the appropriate logging client based on the service or environment."""
    client = ObservabilityClient()

    if service == "datadog":
        return client._get_datadog_client()
    elif service == "google":
        return client._get_google_client()
    elif service == "azure":
        return client._get_azure_client()
    elif service == "aws":
        return client._get_aws_client()
    else:
        # Default to Datadog if no service is specified
        return client._get_datadog_client()
