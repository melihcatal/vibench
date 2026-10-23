import os
import boto3
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient

class SafetyClients:
    """
    Provides configured clients for various content safety services.
    """
    _azure_content_safety_client = None
    _aws_comprehend_client = None

    @classmethod
    def get_azure_content_safety_client(cls) -> ContentSafetyClient:
        if cls._azure_content_safety_client is None:
            endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
            key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
            if not endpoint or not key:
                raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables for Azure Content Safety.")
            cls._azure_content_safety_client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
        return cls._azure_content_safety_client

    @classmethod
    def get_aws_comprehend_client(cls):
        if cls._aws_comprehend_client is None:
            region_name = os.environ.get("AWS_REGION", "us-east-1")
            cls._aws_comprehend_client = boto3.client("comprehend", region_name=region_name)
        return cls._aws_comprehend_client
