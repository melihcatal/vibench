from typing import List
from safety_client import get_content_safety_client
from safety_models import ModerationResult, ModerationCategory
from azure.ai.contentsafety.models import AnalyzeTextOptions


def moderate_batch(texts: List[str]) -> List[ModerationResult]:
    client = get_content_safety_client()
    results = []
    for text in texts:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        categories = []
        for result in response.categories_analysis:
            category_name = result.category.value
            severity = result.severity
            detected = severity > 0
            categories.append(
                ModerationCategory(
                    category=category_name, severity=severity, detected=detected
                )
            )

        results.append(ModerationResult(text=text, categories=categories))
    return results
