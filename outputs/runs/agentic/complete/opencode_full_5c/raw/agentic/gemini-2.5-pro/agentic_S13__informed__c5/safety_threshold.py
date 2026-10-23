from typing import Dict
from azure.ai.contentsafety.models import AnalyzeTextResult


def apply_safety_threshold(
    result: AnalyzeTextResult, thresholds: Dict[str, int]
) -> bool:
    """
    Applies category thresholds to decide whether to allow text.
    A severity score >= threshold means the text is unsafe.
    """
    if not isinstance(result, AnalyzeTextResult):
        raise TypeError("Input must be an Azure AnalyzeTextResult")

    for category_analysis in result.categories_analysis:
        category_name = category_analysis.category.value
        severity = category_analysis.severity

        if category_name in thresholds:
            if severity >= thresholds[category_name]:
                return False  # Unsafe

    return True  # Safe
