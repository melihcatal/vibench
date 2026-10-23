import os
import json


# ----- Amazon CloudWatch Logs (boto3) -----
def get_cw_log_client():
    import boto3

    return boto3.client("logs", region_name=os.getenv("AWS_REGION", "us-east-1"))


# ----- Datadog Logs API (requests) -----
def get_datadog_log_client():
    import requests

    base_url = "https://http-intake.logs.datadoghq.com/v1/input"
    return requests.Session(), base_url


# ----- Google Cloud Logging (google-cloud-logging) -----
def get_gcp_log_client():
    from google.cloud import logging as gcp_logging

    client = gcp_logging.Client()
    return client


# ----- Azure Monitor Logs (azure-monitor-query) -----
def get_azure_log_client():
    from azure.identity import DefaultAzureCredential
    from azure.ai.loganalytics import LogAnalyticsClient

    credential = DefaultAzureCredential()
    return LogAnalyticsClient(
        credential=credential,
        workspace_id=os.getenv("AZURE_LOG_ANALYTICS_WORKSPACE_ID"),
    )


# ----- Datadog client selector (for same-scenario files) -----
# Return the appropriate client based on a configuration variable.
# This helper is referenced by the same-scenario modules.


def get_log_client():
    """Selects the logging service client based on the env variable `LOG_PROVIDER`"""
    provider = os.getenv("LOG_PROVIDER")
    if provider == "cloudwatch":
        return get_cw_log_client()
    if provider == "datadog":
        return get_datadog_log_client()
    if provider == "gcp":
        return get_gcp_log_client()
    if provider == "azure":
        return get_azure_log_client()
    raise ValueError(f"Unsupported LOG_PROVIDER: {provider}")
