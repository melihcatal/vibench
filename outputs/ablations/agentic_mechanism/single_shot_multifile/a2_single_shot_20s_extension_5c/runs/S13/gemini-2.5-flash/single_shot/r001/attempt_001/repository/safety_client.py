import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import dlp_v2, translate_v3
from openai import OpenAI

def get_azure_content_safety_client() -> ContentSafetyClient:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_google_dlp_client() -> dlp_v2.DlpServiceClient:
    # Google Cloud clients typically pick up credentials from GOOGLE_APPLICATION_CREDENTIALS
    # or default service account if running in GCP environment.
    # No explicit project ID needed for client instantiation, but needed for API calls.
    return dlp_v2.DlpServiceClient()

def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    return OpenAI(api_key=api_key)

def get_google_translate_client() -> translate_v3.TranslationServiceClient:
    # Google Cloud clients typically pick up credentials from GOOGLE_APPLICATION_CREDENTIALS
    # or default service account if running in GCP environment.
    return translate_v3.TranslationServiceClient()
