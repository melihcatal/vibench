from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.exceptions import HttpResponseError

from safety_client import get_safety_client
from safety_models import ModerationResult, ContentCategory

def moderate_text(text_to_moderate: str) -> ModerationResult:
    """
    Moderates a single string of text using Azure AI Content Safety.

    Args:
        text_to_moderate: The text to be analyzed.

    Returns:
        A ModerationResult object with the analysis details.
    """
    client = get_safety_client()
    request = AnalyzeTextOptions(text=text_to_moderate)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Error analyzing text: {e}")
        # In a real app, handle this error more gracefully
        raise

    categories = [
        ContentCategory(category=cat.category.value, severity=cat.severity)
        for cat in response.categories_analysis
    ]
    
    passed = all(cat.severity == 0 for cat in categories)

    return ModerationResult(
        text=text_to_moderate,
        categories=categories,
        passed=passed
    )
