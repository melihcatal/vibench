import os
from typing import List
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient, ContentSafetyText
from azure.ai.contentsafety.models import TextCategory
from safety_models import SafetyResult, CategoryScore
from safety_client import compute_rationale


def moderate_text(text: str) -> SafetyResult:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = ContentSafetyText(text)
    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
        TextCategory.SELF_HARM,
    ]
    response = client.analyze_text(request, categories=categories)
    scores = [
        CategoryScore(
            cat_score.category.name.lower().replace("_", "_"),
            cat_score.severity.value / 6.0,
        )
        for cat_score in response.category_scores
    ]
    blocked = any(s.severity > 0.5 for s in scores)
    rationale = compute_rationale(scores, blocked)
    return SafetyResult(
        original_text=text, category_scores=scores, blocked=blocked, rationale=rationale
    )
