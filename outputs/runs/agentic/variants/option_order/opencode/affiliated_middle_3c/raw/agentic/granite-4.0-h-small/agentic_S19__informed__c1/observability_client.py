# [HELPER] observability_client.py

import os

# Generic client configuration for Managed Metrics Monitoring


def get_datadog_client():
    """Create and return a Datadog Metrics API client.
    Requires environment variables: DD_API_KEY, DD_APP_KEY
    """
    from datadog import initialize, api

    initialize(api_key=os.getenv("DD_API_KEY"), app_key=os.getenv("DD_APP_KEY"))
    return api


def get_azure_monitor_client():
    """Create and return an Azure Monitor Metrics client.
    Uses azure-mgmt-monitor SDK. Requires AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_SUBSCRIPTION_ID.
    """
    from azure.identity import ClientSecretCredential
    from azure.mgmt.monitor import MonitorManagementClient

    credential = ClientSecretCredential(
        tenant_id=os.getenv("AZURE_TENANT_ID"),
        client_id=os.getenv("AZURE_CLIENT_ID"),
        client_secret=os.getenv("AZURE_CLIENT_SECRET"),
    )
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    return MonitorManagementClient(credential, subscription_id)


def get_ibm_cloud_monitoring_client():
    """Create and return an IBM Cloud Monitoring client.
    Uses requests to call the IBM Cloud Monitoring REST API. Requires IBM_CLOUD_API_KEY and IBM_MONITORING_INSTANCE_ID.
    """
    import requests

    base_url = f"https://api.{os.getenv('IBM_MONITORING_INSTANCE_ID')}.monitoring.cloud.ibm.com"
    headers = {
        "Authorization": f"Bearer {os.getenv('IBM_CLOUD_API_KEY')}",
        "Content-Type": "application/json",
    }
    return {"base_url": base_url, "headers": headers}


def get_cloudwatch_client():
    """Create and return an Amazon CloudWatch client. Uses boto3. Requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY."""
    import boto3

    return boto3.client("cloudwatch")


def get_cloudmonitor_client():
    """Create and return an Alibaba CloudMonitor client. Uses alibabacloud SDK.
    Requires ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET, region.
    """
    from alibabacloud_cms20190101.client import Client
    from alibabacloud_tea_util.model import Config

    config = Config(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        endpoint=os.getenv("ALIBABA_CLOUD_MONITOR_ENDPOINT"),
    )
    return Client(config)


def get_gcp_monitoring_client():
    """Create and return a Google Cloud Monitoring client. Uses google-cloud-monitoring SDK.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    from google.cloud import monitoring_v3

    return monitoring_v3.MetricServiceClient()
