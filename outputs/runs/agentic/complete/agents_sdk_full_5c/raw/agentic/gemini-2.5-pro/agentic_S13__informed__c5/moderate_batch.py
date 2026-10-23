from typing import List
from safety_client import get_safety_client
from safety_models import ModerationResult, ModerationCategoryResult, ModerationRequest
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.exceptions import HttpResponseError

def moderate_batch(messages: List[ModerationRequest]) -> List[ModerationResult]:
    """
    Moderates a batch of user messages and returns per-message decisions.
    Note: The Azure SDK doesn't have a native batch analysis endpoint,
    so we iterate and call the service for each message.
    """
    client = get_safety_client()
    results = []

    for msg in messages:
        request = AnalyzeTextOptions(text=msg.text)
        try:
            response = client.analyze_text(request)
            
            categories = [
                ModerationCategoryResult(
                    category=result.category.value,
                    severity=result.severity,
                    flagged=result.severity > 0
                )
                for result in response.categories_analysis
            ]
            flagged = any(cat.flagged for cat in categories)
            
            results.append(ModerationResult(
                flagged=flagged,
                categories=categories,
                raw_response=response.to_dict()
            ))

        except HttpResponseError as e:
            print(f"Analyze text failed for text: '{msg.text[:30]}...'. Error: {e.message}")
            results.append(ModerationResult(
                flagged=False,  # Default to not flagged on error
                categories=[],
                raw_response={"error": str(e)}
            ))
            
    return results
