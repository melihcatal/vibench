from translation_client import azure_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import List, Dict


def check_unsafe_content(text: str) -> Dict[str, Any]:
    if not azure_content_safety_client:
        raise ValueError(
            "Azure Content Safety client not initialized. Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )

    request = AnalyzeTextOptions(text=text)

    # Analyze the text for various safety categories
    response = azure_content_safety_client.analyze_text(request)

    # Prepare a dictionary summarizing the moderation results
    safety_results = {
        "hate_score": response.hate_result.severity if response.hate_result else 0,
        "self_harm_score": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual_score": response.sexual_result.severity
        if response.sexual_result
        else 0,
        "violence_score": response.violence_result.severity
        if response.violence_result
        else 0,
    }
    return safety_results
