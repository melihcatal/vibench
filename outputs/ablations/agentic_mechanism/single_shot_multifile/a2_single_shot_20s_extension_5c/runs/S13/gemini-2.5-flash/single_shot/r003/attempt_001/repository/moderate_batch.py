import os
from typing import List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

from safety_client import get_azure_content_safety_client
from safety_models import TextAnalysisResult, ModerationRequest

def moderate_batch(requests: List[ModerationRequest]) -> List[TextAnalysisResult]:
    client = get_azure_content_safety_client()
    results: List[TextAnalysisResult] = []

    for req in requests:
        # Azure Content Safety does not have an explicit batch analyze_text operation
        # for simplicity, we iterate and call the single text API
        # In a real-world scenario, for high throughput, one might manage async calls
        response = client.analyze_text(
            text=req.text
        )

        categories = {
            "Hate": response.hate_result.score if response.hate_result else 0,
            "SelfHarm": response.self_harm_result.score if response.self_harm_result else 0,
            "Sexual": response.sexual_result.score if response.sexual_result else 0,
            "Violence": response.violence_result.score if response.violence_result else 0,
        }

        results.append(
            TextAnalysisResult(
                text=req.text,
                categories=categories,
                is_unsafe=any(score > 0 for score in categories.values())
            )
        )

    return results
