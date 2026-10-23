import boto3
import os

def get_bedrock_runtime_client():
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

def get_bedrock_client():
    return boto3.client(
        service_name="bedrock",
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

def get_translate_client():
    return boto3.client(
        service_name="translate",
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

def get_polly_client():
    return boto3.client(
        service_name="polly",
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

def get_azure_content_safety_client():
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))
