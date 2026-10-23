from typing import List
from safety_client import get_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_models import ModerationResult

def moderate_batch(texts: List[str]) -> List[ModerationResult]:
    """
    Moderates a batch of text strings for unsafe content.

    Note: The Azure Content Safety SDK does not have a native batch endpoint,
    so this function iterates and calls the service for each text.

    :param texts: A list of text strings to moderate.
    :return: A list of ModerationResult objects.
    """
    client = get_safety_client()
    results = []

    for text in texts:
        request = AnalyzeTextOptions(text=text)
        try:
            response = client.analyze_text(request)
            
            is_safe = True
            flagged_categories = []
            for category in response.categories_analysis:
                if category.severity > 0:
                    is_safe = False
                    flagged_categories.append((category.category, category.severity))

            results.append(ModerationResult(
                is_safe=is_safe,
                flagged_categories=flagged_categories,
                raw_response=response.to_dict()
            ))

        except Exception as e:
            results.append(ModerationResult(
                is_safe=False,
                flagged_categories=[("ClientError", str(e))],
                raw_response={"error": str(e)}
            ))
            
    return results
