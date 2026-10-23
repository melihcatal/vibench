import os
from typing import List, Dict, Any
from speech_client import SpeechClient
from speech_models import NormalizedTranscript
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")


def moderate_transcript(segments: NormalizedTranscript) -> List[str]:
    """Runs text moderation on the combined transcript using Azure Content Safety.
    Returns a list of moderated (filtered) text segments.
    """
    client = ContentSafetyClient(
        endpoint=CONTENT_SAFETY_ENDPOINT,
        credential=AzureKeyCredential(CONTENT_SAFETY_KEY),
    )
    text = " ".join([seg["text"] for seg in segments])
    response = client.begin_analyze_text(text).result()
    # Response contains a list of flagged items; if any, we zero‑out the content
    if response.flagged_content:
        return ["<MODERATED>"] * len(segments)
    # If no flags, return original texts
    return [seg["text"] for seg in segments]
