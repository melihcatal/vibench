import os
import boto3
from google.cloud import monitoring_v3
from azure.monitor.query import MonitorQueryClient
from azure.identity import DefaultAzureCredential
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi

def get_gcp_monitoring_client():
    return monitoring_v3.MetricServiceClient()

def get_aws_cloudwatch_client():
    return boto3.client(
        'cloudwatch',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

def get_azure_monitor_client():
    credential = DefaultAzureCredential()
    return MonitorQueryClient(credential=credential)

def get_datadog_metrics_api_client():
    configuration = Configuration(
        api_key={'apiKeyAuth': os.environ.get('DATADOG_API_KEY')},
        server_variables={'site': os.environ.get('DATADOG_SITE', 'datadoghq.com')}
    )
    api_client = ApiClient(configuration)
    return MetricsApi(api_client)