# corpus_safety.py
# LATER-STEP
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def is_corpus_safe(text: str) -> bool:
    """Check corpus text with Azure Content Safety before embedding.

    Returns True if text passes moderation, False otherwise.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not (endpoint and key):
        raise RuntimeError("Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY")
    content_safety_client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    response = content_safety_client.analyze_text(text=text, categories=["text", "html"])
    # Simplify: if any flagged category present, consider unsafe
    unsafe = any(flag for flag in response.flags if flag.name == "unsafe")
    return not unsafe
