import os
from typing import Optional
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient

def get_content_safety_client() -> ContentSafetyClient:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required.")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))
