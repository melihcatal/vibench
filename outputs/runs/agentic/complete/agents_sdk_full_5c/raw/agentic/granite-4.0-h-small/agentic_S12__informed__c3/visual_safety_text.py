# visual_safety_text.py
import os
from typing import List, Dict
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextInput

# Azure Content Safety credentials (set env vars before running)
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

# Initialize the client once (singleton pattern)
_content_safety_client = None

def _get_content_safety_client() -> ContentSafetyClient:
    global _content_safety_client
    if not _content_safety_client:
        _content_safety_client = ContentSafetyClient(
            endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
            credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
        )
    return _content_safety_client


def visual_safety_text(text: List[str]) -> Dict[str, bool]:
    """Check generated visual labels for unsafe / policy‑sensitive language using Azure Content Safety."""
    client = _get_content_safety_client()
    # Merge lines into a single string for moderation
    full_text = " ".join(text)
    response = client.begin_analyze_text(TextInput(text=full_text)).result()
    # The response includes categories such as hate, selfHarm, sexual, violence, etc.
    unsafe_flags = {
        "hate": response.categories.hate.prediction == 1,
        "self_harm": response.categories.self_harm.prediction == 1,
        "sexual": response.categories.sexual.prediction == 1,
        "violence": response.categories.violence.prediction == 1,
        "harassment": response.categories.harassment.prediction == 1
    }
    return unsafe_flags
