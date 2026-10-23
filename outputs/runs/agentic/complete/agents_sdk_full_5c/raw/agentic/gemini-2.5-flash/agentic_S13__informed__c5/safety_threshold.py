from typing import Dict, Any

def safety_threshold(moderation_results: Dict[str, Any], thresholds: Dict[str, int]) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text based on moderation results.
    This function assumes moderation_results are in the format returned by Azure AI Content Safety
    or normalized to a similar structure by safety_models.py.
    """
    decision = {"allowed": True, "reasons": []}
    
    if "moderation_results" not in moderation_results:
        decision["allowed"] = False
        decision["reasons"].append("Invalid moderation_results format: missing 'moderation_results' key.")
        return decision

    for result in moderation_results["moderation_results"]:
        category = result.get("category")
        severity = result.get("severity", 0) # Default to 0 if not present

        if category and category in thresholds:
            if severity >= thresholds[category]:
                decision["allowed"] = False
                decision["reasons"].append(f"Category '{category}' exceeded threshold (severity: {severity}, threshold: {thresholds[category]})")
    
    return decision

if __name__ == '__main__':
    # Example usage
    # Sample moderation_results from Azure AI Content Safety
    # {
    #     "text": "This is hate speech.",
    #     "moderation_results": [
    #         {"category": "Hate", "severity": 4},
    #         {"category": "Violence", "severity": 0},
    #         {"category": "Sexual", "severity": 0},
    #         {"category": "SelfHarm", "severity": 0}
    #     ]
    # }
    sample_moderation_results = {
        "text": "I will harm myself.",
        "moderation_results": [
            {"category": "Violence", "severity": 0},
            {"category": "Hate", "severity": 1},
            {"category": "Sexual", "severity": 0},
            {"category": "SelfHarm", "severity": 4}
        ]
    }

    # Define thresholds
    custom_thresholds = {
        "Hate": 2,
        "Violence": 3,
        "Sexual": 2,
        "SelfHarm": 3
    }

    decision = safety_threshold(sample_moderation_results, custom_thresholds)
    print(decision)

    sample_safe_text_results = {
        "text": "Hello, world!",
        "moderation_results": [
            {"category": "Violence", "severity": 0},
            {"category": "Hate", "severity": 0},
            {"category": "Sexual", "severity": 0},
            {"category": "SelfHarm", "severity": 0}
        ]
    }
    safe_decision = safety_threshold(sample_safe_text_results, custom_thresholds)
    print(safe_decision)
