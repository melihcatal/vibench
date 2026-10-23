import os
from openai import OpenAI, AzureOpenAI
from anthropic import Anthropic
from google.cloud import translate_v3
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import cohere
import boto3
import vertexai

def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key: raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)

def get_anthropic_client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key: raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return Anthropic(api_key=api_key)

def get_vertex_ai_project_location() -> tuple[str, str]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project_id: raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    return project_id, location

def get_azure_openai_client() -> AzureOpenAI:
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.environ.get("AZURE_OPENAI_KEY")
    azure_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
    if not azure_endpoint or not azure_api_key: raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY environment variables not set")
    return AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=azure_api_key,
        api_version=azure_api_version
    )

def get_azure_content_safety_client() -> ContentSafetyClient:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key: raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

def get_google_cloud_translate_client() -> translate_v3.TranslationServiceClient:
    return translate_v3.TranslationServiceClient()

def get_cohere_client() -> cohere.Client:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key: raise ValueError("COHERE_API_KEY environment variable not set")
    return cohere.Client(api_key=api_key)

def get_aws_polly_client():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    if not aws_access_key_id or not aws_secret_access_key: raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables not set")
    return boto3.client(
        "polly",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )