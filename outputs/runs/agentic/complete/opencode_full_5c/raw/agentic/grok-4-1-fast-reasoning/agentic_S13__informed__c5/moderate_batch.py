import os
from typing import List
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory, AnalyzeTextOptions
from safety_models import SafetyResult, SafetyScore

ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
client = None
if ENDPOINT and KEY:
    client = ContentSafetyClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

CATEGORIES = [
    TextCategory.HATE,
    TextCategory.SEXUAL,
    TextCategory.VIOLENCE,
    TextCategory.SELF_HARM,
]


def moderate_batch(texts: List[str]) -> List[SafetyResult]:
    global client
    if client is None:
        raise ValueError(
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY"
        )

    options = AnalyzeTextOptions(categories=CATEGORIES)
    poller = client.analyze_text_bulk(texts=texts, options=options)
    bulk_results = poller.result()

    safety_results: List[SafetyResult] = []
    for idx, result in enumerate(bulk_results):
        scores: List[SafetyScore] = []
        flagged_categories: List[str] = []
        for cat_result in result.categories or []:
            category = cat_result.category.lower()
            severity_value = (
                getattr(cat_result.severity, "value", cat_result.severity or 0) / 6.0
            )
            scores.append({"category": category, "score": float(severity_value)})
            if severity_value > 0.3:
                flagged_categories.append(category)

        blocked = bool(flagged_categories)
        safety_results.append(
            {
                "input_text": texts[idx],
                "blocked": blocked,
                "scores": scores,
                "flagged_categories": flagged_categories,
            }
        )
    return safety_results
