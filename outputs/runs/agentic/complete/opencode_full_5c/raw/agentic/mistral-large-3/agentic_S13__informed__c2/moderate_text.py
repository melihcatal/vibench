from typing import Dict, List, Optional, Union
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
    AnalyzeTextResult,
)


def moderate_text(
    text: str,
    categories: Optional[List[str]] = None,
    block_threshold: Optional[Dict[str, int]] = None,
) -> Dict[str, Union[bool, Dict[str, int]]]:
    """
    Moderate a single text input using Azure AI Content Safety.
    Returns a decision and severity scores for each category.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    azure_categories = {
        "Hate": TextCategory.HATE,
        "SelfHarm": TextCategory.SELF_HARM,
        "Sexual": TextCategory.SEXUAL,
        "Violence": TextCategory.VIOLENCE,
    }

    selected_categories = []
    for cat in categories:
        if cat in azure_categories:
            selected_categories.append(azure_categories[cat])

    if not selected_categories:
        raise ValueError("No valid categories selected")

    request = AnalyzeTextOptions(text=text, categories=selected_categories)
    response: AnalyzeTextResult = client.analyze_text(request)

    scores = {
        "Hate": response.hate_result.severity if response.hate_result else 0,
        "SelfHarm": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "Sexual": response.sexual_result.severity if response.sexual_result else 0,
        "Violence": response.violence_result.severity
        if response.violence_result
        else 0,
    }

    decision = False
    if block_threshold:
        decision = any(
            scores.get(cat, 0) >= threshold
            for cat, threshold in block_threshold.items()
            if cat in scores
        )

    return {
        "decision": decision,
        "scores": scores,
    }
