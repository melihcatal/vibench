# [HELPER] observability_client.py
"""Local configuration and client helper utilities for Managed Log Query / Log Ingestion.
"""

import os
import json
from typing import Any, Dict


def get_logging_client() -> Any:
    """Return a configured logging client instance based on environment variables.

    Supports multiple providers via a simple lookup.
    """
    provider = os.getenv("LOG_PROVIDER", "ibm_cloud_logs")
    if provider == "ibm_cloud_logs":
        # IBM Cloud Logs REST API client (using `requests`)
        import requests

        api_key = os.getenv("IBM_CLOUD_API_KEY")
        instance_id = os.getenv("IBM_LOGS_INSTANCE_ID")
        base_url = f"https://logs.eu-de.logging.ibmcloud.com/api/v1/logs"
        headers = {
            "Authorization": f"IBM IAM {api_key}",
            "Content-Type": "application/json",
        }
        class IBMLogsClient:
            def post(self, endpoint: str, json: Dict[str, Any], headers: Dict[str, str]) -> Any:
                return requests.post(base_url + endpoint, json=json, headers=headers)
                
        return IBMLogsClient()
    elif provider == "alibaba_log_service":
        # Alibaba Simple Log Service client (using `aliyun-log-python-sdk`)
        from aliyunsdkcore.client import AcsClient
        from aliyunsdklog.request.v20170901 import PutLogsRequest

        access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        client = AcsClient(access_key_id, access_key_secret, "cn-hangzhou")
        return client
    elif provider == "aws_cloudwatch":
        # Amazon CloudWatch Logs client (using `boto3`)
        import boto3
        client = boto3.client(
            "logs",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        return client
    elif provider == "azure_monitor":
        # Azure Monitor Logs client (using `azure-monitor-ingestion` and `azure-monitor-query`)
        from azure.monitor.ingestion import LogsIngestionClient
        from azure.monitor.query import LogsQueryClient
        from azure.identity import DefaultAzureCredential
        credential = DefaultAzureCredential()
        logs_ingest = LogsIngestionClient(
            endpoint="https://уникс.ingest.monitor.azure.com",
            credential=credential,
        )
        logs_query = LogsQueryClient(
            endpoint="https://уникс.monitor.azure.com",
            credential=credential,
        )
        return {
            "ingest": logs_ingest,
            "query": logs_query,
        }
    elif provider == "datadog":
        # Datadog Logs API client (using `requests`)
        import requests
        api_key = os.getenv("DD_API_KEY")
        app_key = os.getenv("DD_APP_KEY")
        headers = {
            "DD-API-KEY": api_key,
            "DD-APPLICATION-KEY": app_key,
            "Content-Type": "application/json",
        }
        return {
            "client": requests,
            "headers": headers,
        }
    elif provider == "google_logging":
        # Google Cloud Logging client (using `google-cloud-logging`)
        from google.cloud import logging as glog
        client = glog.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
        return client
    else:
        raise ValueError(f"Unsupported LOG_PROVIDER: {provider}
Supported values: ibm_cloud_logs, alibaba_log_service, aws_cloudwatch, azure_monitor, datadog, google_logging")
