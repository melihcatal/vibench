from typing import Dict, Tuple

from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.exceptions import HttpResponseError

from safety_client import get_azure_safety_client


def apply_safety_thresholds(text: str, thresholds: Dict[str, int]) -> Tuple[bool, Dict[str, str]]:
    """
    Applies custom category severity thresholds to decide whether to allow text.
    
    Args:
        text: The input text to analyze.
        thresholds: A dictionary mapping category names (e.g., "Hate") to a
                    maximum allowed severity level (integer).

    Returns:
        A tuple containing:
        - A boolean indicating if the text is allowed (True) or not (False).
        - A dictionary of categories that violated their thresholds.
    """
    client = get_azure_safety_client()
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed. Reason: {e.reason}")
        # Fail closed on analysis error
        return False, {"error": f"API call failed: {e.reason}"}

    violations = {}
    is_allowed = True

    for category_result in response.categories_analysis:
        category_name = category_result.category.value
        if category_name in thresholds:
            if category_result.severity > thresholds[category_name]:
                is_allowed = False
                violations[category_name] = f"Severity {category_result.severity} exceeds threshold {thresholds[category_name]}"

    return is_allowed, violations
