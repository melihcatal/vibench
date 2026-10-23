from safety_client import get_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_models import ModerationResult

def moderate_text(text: str) -> ModerationResult:
    """
    Moderates a single string of text for unsafe content.

    :param text: The text to moderate.
    :return: A ModerationResult object with the outcome.
    """
    client = get_safety_client()
    request = AnalyzeTextOptions(text=text)
    
    try:
        response = client.analyze_text(request)
    except Exception as e:
        # Handle client-side or network errors
        return ModerationResult(
            is_safe=False, 
            flagged_categories=[("Error", str(e))],
            raw_response={"error": str(e)}
        )

    flagged_categories = []
    is_safe = True
    for category in response.categories_analysis:
        if category.severity > 0:
            is_safe = False
            flagged_categories.append((category.category, category.severity))
            
    return ModerationResult(
        is_safe=is_safe,
        flagged_categories=flagged_categories,
        raw_response=response.to_dict()
    )
