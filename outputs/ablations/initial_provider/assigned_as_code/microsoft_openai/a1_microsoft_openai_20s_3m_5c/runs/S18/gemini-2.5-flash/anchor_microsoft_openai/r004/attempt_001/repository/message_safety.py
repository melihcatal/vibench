import os
from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from messaging_models import ContentSafetyRequest, ContentSafetyResponse

def check_message_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # The categories to be analyzed in the text.
    categories = [
        TextCategory.VIOLENCE,
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ]

    # The a new AnalyzeTextOptions object
    request_options = AnalyzeTextOptions(text=request.text, categories=categories)

    # Analyze the text for harmful content.
    response = client.analyze_text(request_options)

    is_safe = True
    moderation_results = {}

    for category_result in response.categories_analysis:
        if category_result.severity > 0:
            is_safe = False
        moderation_results[str(category_result.category)] = {
            "severity": category_result.severity,
            "detected": category_result.severity > 0
        }
    
    return ContentSafetyResponse(is_safe=is_safe, moderation_results=moderation_results)
