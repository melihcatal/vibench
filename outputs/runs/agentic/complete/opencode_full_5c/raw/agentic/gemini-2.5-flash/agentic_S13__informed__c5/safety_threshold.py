from typing import List, Dict
from safety_models import TextModerationResponse, ModerationDecision, ThresholdConfig


def apply_safety_thresholds(
    response: TextModerationResponse, thresholds: List[ThresholdConfig]
) -> ModerationDecision:
    """Applies category thresholds to decide whether to allow text.

    This function assumes that the severity returned by the moderation service is a numerical score
    where higher is more severe. A threshold defines the maximum allowed severity for a category.
    If any category's severity exceeds its threshold, the text is considered unsafe.
    """
    is_safe = True
    category_scores: Dict[str, float] = {}

    for category_analysis_key, analysis_data in response.categories_analysis.items():
        # Assuming 'severity' is the key for the score in analysis_data
        severity = analysis_data.get("severity", 0.0)
        category_scores[category_analysis_key] = float(severity)

    for threshold_config in thresholds:
        category = threshold_config.category
        threshold_value = threshold_config.threshold

        if category in category_scores and category_scores[category] >= threshold_value:
            is_safe = False
            break

    # The original text is not directly available in TextModerationResponse,
    # so we'll use a placeholder or assume it's passed separately if needed in a real scenario.
    # For this example, we'll use a generic placeholder.
    original_text = "N/A"

    return ModerationDecision(
        text=original_text, is_safe=is_safe, categories_scores=category_scores
    )
