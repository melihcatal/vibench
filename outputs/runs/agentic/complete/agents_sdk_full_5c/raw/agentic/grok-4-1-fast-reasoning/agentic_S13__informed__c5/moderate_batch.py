import os
from typing import List, Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import DEFAULT_THRESHOLDS
from safety_models import normalize_safety_scores

def moderate_batch(texts: List[str]) -> List[Dict[str, Any]]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY required.")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    categories = [TextCategory.HATE, TextCategory.SEXUAL, TextCategory.VIOLENCE, TextCategory.SELF_HARM]
    results = []
    for text in texts:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request, categories=categories)
        scores = {}
        for cat in categories:
            cat_result = getattr(response, cat.value.lower())
            severity = cat_result.severity if cat_result and cat_result.severity is not None else 0
            scores[cat.value.lower()] = float(severity) / 4.0
        results.append(normalize_safety_scores(scores, DEFAULT_THRESHOLDS))
    return results