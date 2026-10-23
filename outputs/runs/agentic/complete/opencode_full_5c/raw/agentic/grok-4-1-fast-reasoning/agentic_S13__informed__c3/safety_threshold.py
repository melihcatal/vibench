import os
from typing import Dict, List
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import DEFAULT_THRESHOLDS
from safety_models import ThresholdDecision, SafetyScores


def safety_threshold(
    text: str, category_thresholds: Dict[str, float] | None = None
) -> ThresholdDecision:
    if category_thresholds is None:
        category_thresholds = DEFAULT_THRESHOLDS
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
    scores: SafetyScores = {
        "hate": result.hate.score if result.hate else 0.0,
        "sexual": result.sexual.score if result.sexual else 0.0,
        "violence": result.violence.score if result.violence else 0.0,
        "self_harm": result.self_harm.score if result.self_harm else 0.0,
    }
    violated_categories = [
        cat
        for cat, score in scores.items()
        if score > category_thresholds.get(cat, 0.0)
    ]
    allow = len(violated_categories) == 0
    return {
        "allow": allow,
        "violated_categories": violated_categories,
        "scores": scores,
    }
