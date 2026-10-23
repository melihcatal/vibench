import os
from typing import List
from speech_models import TranscriptionResult
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def moderate_transcript(transcript: str) -> str:
    """Moderate the raw transcript and return a clean version.

    Uses Azure Content Safety to detect and remove toxic content.
    """
    client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY")),
    )
    response = client.analyze_text_toxicity_text(content=transcript)
    cleaned_text = response.safe_content
    return cleaned_text


# Example
# clean = moderate_transcript(raw_transcript)
