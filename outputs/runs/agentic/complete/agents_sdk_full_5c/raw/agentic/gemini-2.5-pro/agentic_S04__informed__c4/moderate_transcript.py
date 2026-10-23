import os
from typing import List, Dict
from speech_models import TranscriptSegment

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_transcript(transcript_text: str) -> Dict:
    """
    Moderates transcript text using Azure AI Content Safety.

    Args:
        transcript_text: The text content of the transcript.

    Returns:
        A dictionary containing the moderation analysis results.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=transcript_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed. Reason: {e.reason}")
        raise

    return {
        "hate_result": response.hate_result.severity if response.hate_result else 0,
        "self_harm_result": response.self_harm_result.severity if response.self_harm_result else 0,
        "sexual_result": response.sexual_result.severity if response.sexual_result else 0,
        "violence_result": response.violence_result.severity if response.violence_result else 0,
    }
