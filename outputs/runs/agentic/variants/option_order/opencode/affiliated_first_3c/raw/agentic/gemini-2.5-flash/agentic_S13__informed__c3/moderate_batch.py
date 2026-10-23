from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_content_safety_client
from safety_models import TextModerationResponse, ModerationResult


def moderate_batch(texts: List[str]) -> List[TextModerationResponse]:
    client = get_content_safety_client()
    batch_results = []

    for text in texts:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        results = []
        for category_result in response.categories_analysis:
            results.append(
                ModerationResult(
                    category=category_result.category.value,
                    severity=category_result.severity,
                    detected=category_result.severity > 0,
                )
            )
        batch_results.append(TextModerationResponse(text=text, results=results))

    return batch_results
