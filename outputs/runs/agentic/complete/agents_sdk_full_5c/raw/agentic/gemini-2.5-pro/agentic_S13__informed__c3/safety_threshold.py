from typing import Dict
from safety_client import get_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_models import ThresholdDecision

def apply_safety_threshold(text: str, thresholds: Dict[str, int]) -> ThresholdDecision:
    """
    Applies custom severity thresholds to moderation results.

    :param text: The text to analyze.
    :param thresholds: A dictionary mapping category names (e.g., 'Hate', 'Sexual')
                       to maximum allowed severity scores (integer).
    :return: A ThresholdDecision object indicating if the text should be allowed.
    """
    client = get_safety_client()
    request = AnalyzeTextOptions(text=text)
    
    try:
        response = client.analyze_text(request)
    except Exception as e:
        return ThresholdDecision(allow=False, violated_categories=[("ClientError", str(e))])

    violated_categories = []
    allow = True

    for category_result in response.categories_analysis:
        category_name = category_result.category.value
        severity = category_result.severity
        
        if category_name in thresholds and severity >= thresholds[category_name]:
            allow = False
            violated_categories.append((category_name, severity))
            
    return ThresholdDecision(
        allow=allow,
        violated_categories=violated_categories
    )
