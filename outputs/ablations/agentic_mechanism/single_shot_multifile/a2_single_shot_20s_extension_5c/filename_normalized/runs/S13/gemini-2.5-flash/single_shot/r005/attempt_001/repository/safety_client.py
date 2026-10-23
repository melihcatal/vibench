import os
from openai import OpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import dlp_v2, translate_v3
import boto3
import anthropic
import cohere

def load_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key: raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)

def load_azure_content_safety_client() -> ContentSafetyClient:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key: raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set.")
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def load_google_dlp_client() -> dlp_v2.DlpServiceClient:
    # Google Cloud clients typically pick up credentials from environment (GOOGLE_APPLICATION_CREDENTIALS) or metadata service
    # No explicit key/endpoint needed if authenticated via standard GCP methods.
    return dlp_v2.DlpServiceClient()

def load_aws_ssm_client():
    # AWS clients pick up credentials from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION) or metadata service
    return boto3.client('ssm', region_name=os.environ.get("AWS_REGION", "us-east-1"))

def load_anthropic_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key: raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
    return anthropic.Anthropic(api_key=api_key)

def load_google_translate_client() -> translate_v3.TranslationServiceClient:
    # Google Cloud clients typically pick up credentials from environment or metadata service
    return translate_v3.TranslationServiceClient()

def load_cohere_client() -> cohere.Client:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key: raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key=api_key)

def load_aws_polly_client():
    # AWS clients pick up credentials from environment or metadata service
    return boto3.client('polly', region_name=os.environ.get("AWS_REGION", "us-east-1"))
