import os
import boto3
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import dlp_v2, translate_v3
from openai import OpenAI

def get_azure_content_safety_client() -> ContentSafetyClient:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

def get_google_dlp_client() -> dlp_v2.DlpServiceClient:
    # GOOGLE_APPLICATION_CREDENTIALS should be set for authentication
    return dlp_v2.DlpServiceClient()

def get_aws_ssm_client():
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION_NAME env vars or IAM role
    return boto3.client('ssm', region_name=os.environ.get("AWS_REGION_NAME", "us-east-1"))

def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    return OpenAI(api_key=api_key)

def get_google_translate_client() -> translate_v3.TranslationServiceClient:
    # GOOGLE_APPLICATION_CREDENTIALS should be set for authentication
    return translate_v3.TranslationServiceClient()

def get_aws_polly_client():
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_REGION_NAME env vars or IAM role
    return boto3.client('polly', region_name=os.environ.get("AWS_REGION_NAME", "us-east-1"))
