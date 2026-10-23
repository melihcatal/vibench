from typing import Dict
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.exceptions import HttpResponseError

from safety_client import get_safety_client

# Default thresholds if none are provided. A higher value means less strict.
# Azure severity scores range from 0 (safe) to 6 (high risk).
# A threshold of 2 means severities 0 and 1 will pass.
DEFAULT_THRESHOLDS = {
    TextCategory.HATE: 2,
    TextCategory.SELF_HARM: 2,
    TextCategory.SEXUAL: 4,
    TextCategory.VIOLENCE: 2,
}

def apply_safety_threshold(text: str, thresholds: Dict[TextCategory, int] = None) -> bool:
    """
    Applies custom severity thresholds to a text moderation result.

    Args:
        text: The text to analyze.
        thresholds: A dictionary mapping TextCategory to an integer severity threshold.
                    If a category's severity is above its threshold, the text fails.

    Returns:
        True if the text is within all thresholds, False otherwise.
    """
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    client = get_safety_client()
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Error applying thresholds: {e}")
        return False # Fail on error

    for category_analysis in response.categories_analysis:
        category = category_analysis.category
        severity = category_analysis.severity
        
        if category in thresholds and severity > thresholds[category]:
            print(f"'{category.value}' severity {severity} exceeds threshold {thresholds[category]}")
            return False

    return True
