import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from safety_client import get_azure_credentials
from safety_models import ModerationResult, SafetyRating

def moderate_text(text_to_moderate: str) -> ModerationResult:
    """
    Moderates a single piece of text using Azure AI Content Safety.
    """
    endpoint, key = get_azure_credentials()
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text_to_moderate)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        # Return a default 'safe' result on error
        return ModerationResult(
            flagged=False,
            categories={},
            ratings=[]
        )

    flagged = any(cat.severity > 0 for cat in response.categories_analysis)
    
    categories = {
        TextCategory.HATE: response.hate_result.severity if response.hate_result else 0,
        TextCategory.SELF_HARM: response.self_harm_result.severity if response.self_harm_result else 0,
        TextCategory.SEXUAL: response.sexual_result.severity if response.sexual_result else 0,
        TextCategory.VIOLENCE: response.violence_result.severity if response.violence_result else 0,
    }
    
    ratings = [
        SafetyRating(category=cat.category, severity=cat.severity)
        for cat in response.categories_analysis
    ]

    return ModerationResult(
        flagged=flagged,
        categories=categories,
        ratings=ratings
    )
