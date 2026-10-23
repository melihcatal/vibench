from typing import Dict, List
from safety_models import ModerationResult, ThresholdDecision, TextCategory

def apply_thresholds(moderation_result: ModerationResult, threshold_map: Dict[str, int]) -> ThresholdDecision:
    flagged_categories: List[TextCategory] = []
    decision = "ALLOW"

    for category_analysis in moderation_result.categories:
        category_name = category_analysis.category
        severity = category_analysis.severity

        if category_name in threshold_map:
            if severity >= threshold_map[category_name]:
                flagged_categories.append(category_analysis)
                decision = "FLAG"
    
    return ThresholdDecision(text=moderation_result.text, decision=decision, flagged_categories=flagged_categories)
