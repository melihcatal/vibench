import os
from google.cloud import dlp_v2, translate_v3
import azure.ai.contentsafety as azcs
import openai
import cohere
from elevenlabs.client import ElevenLabs
import boto3

def get_azure_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")
    from azure.core.credentials import AzureKeyCredential
    return azcs.ContentSafetyClient(endpoint, AzureKeyCredential(key))

def get_google_dlp_client():
    return dlp_v2.DlpServiceClient()

def get_aws_secrets_manager_client():
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region)

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set.")
    return openai.OpenAI(api_key=api_key)

def get_google_translate_client():
    return translate_v3.TranslationServiceClient()

def get_cohere_client():
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set.")
    return cohere.Client(api_key=api_key)

def get_elevenlabs_client():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY must be set.")
    return ElevenLabs(api_key=api_key)