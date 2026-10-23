import os
from typing import Dict, Any

def get_azure_content_safety_client() -> Any:
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

def get_perspective_api_key() -> str:
    key = os.getenv("PERSPECTIVE_API_KEY")
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY must be set")
    return key

def get_tisane_headers() -> Dict[str, str]:
    key = os.getenv("TISANE_API_KEY")
    if not key:
        raise ValueError("TISANE_API_KEY must be set")
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }