from safety_client import get_safety_client
from safety_models import ModerationResult, ModerationCategoryResult
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.exceptions import HttpResponseError

def moderate_text(text: str) -> ModerationResult:
    """
    Scores a single string for unsafe or policy-violating content.
    """
    client = get_safety_client()
    
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e.message}")
        # Return a default 'safe' result on error
        return ModerationResult(flagged=False, categories=[], raw_response=str(e))

    categories = [
        ModerationCategoryResult(
            category=result.category.value, 
            severity=result.severity,
            flagged=result.severity > 0
        )
        for result in response.categories_analysis
    ]
    
    flagged = any(cat.flagged for cat in categories)

    return ModerationResult(
        flagged=flagged,
        categories=categories,
        raw_response=response.to_dict()
    )
