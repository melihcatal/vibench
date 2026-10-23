from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.exceptions import HttpResponseError

from safety_client import get_safety_client
from safety_models import ModerationResult, BatchModerationResult, ContentCategory

def moderate_batch(texts_to_moderate: List[str]) -> BatchModerationResult:
    """
    Moderates a batch of text strings by iterating and calling the service for each.

    Args:
        texts_to_moderate: A list of text strings to analyze.

    Returns:
        A BatchModerationResult object containing a list of individual results.
    """
    client = get_safety_client()
    results = []

    for text in texts_to_moderate:
        request = AnalyzeTextOptions(text=text)
        try:
            response = client.analyze_text(request)
            categories = [
                ContentCategory(category=cat.category.value, severity=cat.severity)
                for cat in response.categories_analysis
            ]
            passed = all(cat.severity == 0 for cat in categories)
            result = ModerationResult(
                text=text,
                categories=categories,
                passed=passed
            )
            results.append(result)
        except HttpResponseError as e:
            # Handle or log the error for the specific text message
            print(f"Failed to process text '{text[:30]}...': {e}")
            # Optionally add a failure result to the list
            results.append(ModerationResult(text=text, passed=False, categories=[]))

    return BatchModerationResult(results=results)
