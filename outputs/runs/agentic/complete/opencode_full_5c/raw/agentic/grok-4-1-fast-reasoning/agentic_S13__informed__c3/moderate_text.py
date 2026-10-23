import os
from typing import Dict
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_text(text: str) -> Dict[str, float]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
        TextCategory.SELF_HARM,
    ]
    options = AnalyzeTextOptions(categories=categories)
    poller = client.analyze_text(text, options)
    result = poller.result()
    scores = {
        "hate": result.hate.score if result.hate else 0.0,
        "sexual": result.sexual.score if result.sexual else 0.0,
        "violence": result.violence.score if result.violence else 0.0,
        "self_harm": result.self_harm.score if result.self_harm else 0.0,
    }
    return scores
