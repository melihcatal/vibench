import os
from openai import OpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def get_openai_client():
    """Initializes and returns the OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)

def get_azure_content_safety_client():
    """Initializes and returns the Azure Content Safety client."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set.")
    
    return ContentSafetyClient(endpoint, AzureKeyCredential(api_key))
