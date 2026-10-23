import os
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from speech_models import SafetyAnalysisResult

def check_live_caption_safety(transcript_text: str) -> SafetyAnalysisResult:
    """
    Checks live transcript text for unsafe content using Azure AI Content Safety.

    Args:
        transcript_text: The text chunk from the live transcript.

    Returns:
        A SafetyAnalysisResult object.
    """
    load_dotenv()
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=transcript_text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return SafetyAnalysisResult(is_safe=True, harm_categories={}) # Fail open

    is_safe = all(
        category.severity == 0
        for category in [
            response.hate_result,
            response.harassment_result,
            response.self_harm_result,
            response.sexual_result,
            response.violence_result,
        ]
    )
    
    harm_categories = {
        "hate": response.hate_result.severity,
        "harassment": response.harassment_result.severity,
        "self_harm": response.self_harm_result.severity,
        "sexual": response.sexual_result.severity,
        "violence": response.violence_result.severity,
    }

    return SafetyAnalysisResult(is_safe=is_safe, harm_categories=harm_categories)
