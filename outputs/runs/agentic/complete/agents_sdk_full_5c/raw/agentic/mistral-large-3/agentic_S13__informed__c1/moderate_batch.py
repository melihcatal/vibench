import os
from typing import List, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_batch(texts: List[str]) -> List[Dict[str, Any]]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    results = []

    for text in texts:
        request = AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE
            ],
            output_type="EightSeverityLevels"
        )
        response = client.analyze_text(request)
        results.append({
            "hate": response.hate_result.severity if response.hate_result else 0,
            "self_harm": response.self_harm_result.severity if response.self_harm_result else 0,
            "sexual": response.sexual_result.severity if response.sexual_result else 0,
            "violence": response.violence_result.severity if response.violence_result else 0
        })

    return results