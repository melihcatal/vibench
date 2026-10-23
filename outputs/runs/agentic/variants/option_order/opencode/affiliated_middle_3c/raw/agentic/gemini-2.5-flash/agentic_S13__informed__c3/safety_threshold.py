from typing import List
from safety_models import ModerationResult, ModerationCategory


def apply_safety_thresholds(
    result: ModerationResult, category_thresholds: List[ModerationCategory]
) -> ModerationResult:
    decision = "Accept"
    for threshold_item in category_thresholds:
        for analysis_item in result.categories_analysis:
            if (
                analysis_item.category == threshold_item.category
                and analysis_item.severity >= threshold_item.severity
            ):
                decision = "Reject"
                break  # Found a rejection, no need to check other categories for this threshold_item
        if decision == "Reject":
            break  # Already rejected, no need to check other threshold_items

    result.overall_decision = decision
    return result
