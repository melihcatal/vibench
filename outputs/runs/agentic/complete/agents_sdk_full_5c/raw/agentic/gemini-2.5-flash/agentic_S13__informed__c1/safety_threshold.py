import os
from typing import Dict, Any
from safety_models import ModerationResult # Assuming safety_models.py defines ModerationResult

# Although this file defines local logic, it implies the use of
# a content safety provider whose output it processes. 
# For example, it relies on the category names and severity levels
# from Azure AI Content Safety, referenced by environment variables.
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

def apply_category_thresholds(moderation_results: Dict[str, int], thresholds: Dict[str, int]) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text.
    moderation_results: A dictionary where keys are category names (e.g., 'Hate', 'SelfHarm')
                        and values are their severity scores (e.g., 0-4).
    thresholds: A dictionary where keys are category names and values are the maximum
                allowed severity for that category.
    Returns a dictionary indicating overall decision and per-category decisions.
    """
    decision = {"overall_allowed": True, "category_decisions": {}}

    for category, severity in moderation_results.items():
        allowed_severity = thresholds.get(category, -1) # -1 if no threshold defined, meaning always allowed or handled differently
        is_allowed = severity <= allowed_severity if allowed_severity != -1 else True
        decision["category_decisions"][category] = {
            "severity": severity,
            "threshold": allowed_severity,
            "allowed": is_allowed
        }
        if not is_allowed:
            decision["overall_allowed"] = False
            
    return decision

if __name__ == '__main__':
    # Example usage based on Azure AI Content Safety output structure
    sample_moderation_results = {
        "Hate": 0,
        "Sexual": 1,
        "SelfHarm": 3,
        "Violence": 0
    }

    # Example thresholds (e.g., max severity 2 for 'SelfHarm', 1 for 'Sexual')
    sample_thresholds = {
        "Hate": 3,
        "Sexual": 1,
        "SelfHarm": 2,
        "Violence": 3
    }

    decision = apply_category_thresholds(sample_moderation_results, sample_thresholds)
    print("Moderation Decision:", decision)

    # Another example
    sample_moderation_results_2 = {
        "Hate": 4,
        "Sexual": 0,
        "SelfHarm": 0,
        "Violence": 0
    }
    decision_2 = apply_category_thresholds(sample_moderation_results_2, sample_thresholds)
    print("\nModeration Decision 2:", decision_2)
