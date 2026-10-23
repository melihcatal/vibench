from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_safety_client
from safety_models import BatchModerationResult, ModerationResult


def moderate_batch(texts: List[str]) -> BatchModerationResult:
    """
    Moderates a batch of text messages for unsafe content.
    """
    client = get_safety_client()
    results = []

    for text in texts:
        request = AnalyzeTextOptions(text=text)
        try:
            response = client.analyze_text(request)
            passed = all(
                category.severity == 0 for category in response.categories_analysis
            )
            scores = {
                category.category.value: category.severity
                for category in response.categories_analysis
            }
            results.append(
                ModerationResult(passed=passed, category_scores=scores, text=text)
            )
        except Exception:
            results.append(
                ModerationResult(passed=False, category_scores={"error": -1}, text=text)
            )

    return BatchModerationResult(results=results)
