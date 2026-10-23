from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_safety_client
from safety_models import ModerationResult


def moderate_text(text: str) -> ModerationResult:
    """
    Moderates a single piece of text for unsafe content.
    """
    client = get_safety_client()
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except Exception as e:
        # Handle potential API errors
        return ModerationResult(passed=False, category_scores={"error": -1}, text=text)

    passed = all(category.severity == 0 for category in response.categories_analysis)

    scores = {
        category.category.value: category.severity
        for category in response.categories_analysis
    }

    return ModerationResult(passed=passed, category_scores=scores, text=text)
