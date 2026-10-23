import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_live_caption_safety(transcript_text: str):
    """
    Analyzes a transcript chunk for unsafe content using Azure Content Safety.

    Args:
        transcript_text: The text chunk from the live transcript.

    Returns:
        A dictionary with the analysis results.
    """
    try:
        key = os.environ["CONTENT_SAFETY_KEY"]
        endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]
    except KeyError:
        raise EnvironmentError("Missing CONTENT_SAFETY_KEY or CONTENT_SAFETY_ENDPOINT environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=transcript_text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return None

    return {
        "hate": response.hate_result.severity,
        "self_harm": response.self_harm_result.severity,
        "sexual": response.sexual_result.severity,
        "violence": response.violence_result.severity,
    }
