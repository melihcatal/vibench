import os
import boto3
from google.cloud import logging as gcp_logging
from azure.core.credentials import AzureKeyCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.translation.text import TranslatorTextClient
import ibm_watsonx_ai as wml


def get_cloudwatch_logs_client():
    """Configure and return a boto3 CloudWatch Logs client using AWS credentials."""
    return boto3.client(
        "logs",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def get_gcp_logging_client():
    """Return a Google Cloud Logging client using APPLICATION_CREDENTIALS."""
    return gcp_logging.Client()


def get_azure_ingestion_client():
    """Return an Azure Monitor Logs ingestion client with connection string."""
    connection_string = os.getenv("AZURE_MONITOR_CONNECTION_STRING")
    return LogsIngestionClient.from_connection_string(connection_string)


def get_azure_content_safety_client():
    """Return an Azure Content Safety client for toxicity checks."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))


def get_azure_translation_client():
    """Return an Azure Translator client for text translation."""
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    return TranslatorTextClient(endpoint, AzureKeyCredential(key))


def get_watsonx_embedding_config():
    """Return WatsonX embeddings configuration from env vars."""
    return {
        "endpoint": os.getenv("WATSONX_API_ENDPOINT"),
        "api_key": os.getenv("WATSONX_API_KEY"),
        "project_id": os.getenv("WATSONX_PROJECT_ID"),
    }


# Helper to load Datadog config if needed (not used in current files)
