import os
from typing import Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

from safety_client import get_azure_content_safety_client
from safety_models import TextAnalysisResult

def moderate_text(text_content: str) -> TextAnalysisResult:
    client = get_azure_content_safety_client()

    # Azure Content Safety uses the `analyze_text` operation
    response = client.analyze_text(
        text=text_content
    )

    categories = {
        "Hate": response.hate_result.score if response.hate_result else 0,
        "SelfHarm": response.self_harm_result.score if response.self_harm_result else 0,
        "Sexual": response.sexual_result.score if response.sexual_result else 0,
        "Violence": response.violence_result.score if response.violence_result else 0,
    }

    return TextAnalysisResult(
        text=text_content,
        categories=categories,
        is_unsafe=any(score > 0 for score in categories.values()) # Simple check, actual decision made in safety_threshold.py
    )
