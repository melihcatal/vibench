import os
from typing import List
from speech_client import get_text_to_speech_client
from speech_models import OutputFormat

def check_safety(script: str, block_bad_content: bool = True) -> bool:
    """
    Detect unsafe content using Azure AI Content Safety.
    Returns True if the text is safe, False if blocked.
    """
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise RuntimeError("Azure Content Safety credentials (endpoint & key) must be set.")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    response = client.analyze_text_sync(text=script)
    safe = response.category == "safe"
    if not safe and block_bad_content:
        print("Unsafe content detected:", response.category)
    return safe
