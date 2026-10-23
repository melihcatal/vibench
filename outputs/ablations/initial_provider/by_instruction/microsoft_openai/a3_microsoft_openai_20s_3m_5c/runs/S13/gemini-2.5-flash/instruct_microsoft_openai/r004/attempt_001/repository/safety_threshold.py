from typing import Dict
from safety_models import TextModerationResponse

def apply_safety_thresholds(response: TextModerationResponse, thresholds: Dict[str, int]) -> bool:
    if not response.categories:
        return True  # No issues found, allow by default

    for category_result in response.categories:
        category_name = category_result.get("category")
        severity = category_result.get("severity", 0)
        
        if category_name and category_name in thresholds:
            if severity >= thresholds[category_name]:
                return False  # Block if severity meets or exceeds the threshold
    return True  # Allow if no thresholds are met or exceeded
