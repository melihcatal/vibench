from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import os

from google.cloud import monitoring_v3
import boto3
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from azure.storage.blob import BlobServiceClient
import openai
import deepl


class ClientFactory:
    @staticmethod
    def get_google_monitoring_client():
        """Returns a Google Cloud Monitoring client."""
        return monitoring_v3.MetricServiceClient()

    @staticmethod
    def get_aws_cloudwatch_client():
        """Returns an AWS CloudWatch client."""
        return boto3.client(
            "cloudwatch",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

    @staticmethod
    def get_datadog_metrics_api():
        """Returns a Datadog Metrics API client."""
        configuration = Configuration()
        api_client = ApiClient(configuration)
        return MetricsApi(api_client)

    @staticmethod
    def get_dynatrace_api_token():
        """Returns the Dynatrace API token from environment variables."""
        return os.environ.get("DYNATRACE_API_TOKEN")

    @staticmethod
    def get_dynatrace_environment_id():
        """Returns the Dynatrace environment ID."""
        return os.environ.get("DYNATRACE_ENVIRONMENT_ID")

    @staticmethod
    def get_azure_blob_service_client():
        """Returns an Azure Blob Storage service client."""
        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not set.")
        return BlobServiceClient.from_connection_string(connection_string)

    @staticmethod
    def get_openai_client():
        """Initializes and returns the OpenAI client."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        return openai.OpenAI(api_key=api_key)

    @staticmethod
    def get_deepl_translator():
        """Initializes and returns the DeepL translator client."""
        auth_key = os.environ.get("DEEPL_AUTH_KEY")
        if not auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        return deepl.Translator(auth_key)
