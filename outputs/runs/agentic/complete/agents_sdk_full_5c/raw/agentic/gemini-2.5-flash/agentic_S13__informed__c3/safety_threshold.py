from typing import Dict, Any
from safety_models import ContentSafetyResponse

def safety_threshold(moderation_result: ContentSafetyResponse, thresholds: Dict[str, int]) -> bool:
    """Applies category thresholds to decide whether to allow text.

    Args:
        moderation_result: The moderation scores from a service like Azure AI Content Safety.
        thresholds: A dictionary of category names to their maximum allowed severity.

    Returns:
        True if the text is allowed based on thresholds, False otherwise.
    """
    # Ensure moderation_result is not None or an error state
    if moderation_result.error:
        print(f"Moderation result contains an error: {moderation_result.error}")
        return False # Deny by default on error

    # Check each category against its threshold
    if "Hate" in thresholds and moderation_result.hate_severity >= thresholds["Hate"]:
        return False
    if "SelfHarm" in thresholds and moderation_result.self_harm_severity >= thresholds["SelfHarm"]:
        return False
    if "Sexual" in thresholds and moderation_result.sexual_severity >= thresholds["Sexual"]:
        return False
    if "Violence" in thresholds and moderation_result.violence_severity >= thresholds["Violence"]:
        return False

    return True

if __name__ == "__main__":
    # Example usage
    # This function uses the output of Azure AI Content Safety implicitly via ContentSafetyResponse.
    # It doesn't directly call the Azure API, but depends on its output format.

    # Example moderation result (from Azure AI Content Safety)
    # This assumes moderate_text.py would return a ContentSafetyResponse instance
    example_safe_result = ContentSafetyResponse(
        hate_severity=0,
        self_harm_severity=0,
        sexual_severity=0,
        violence_severity=0
    )

    example_unsafe_result = ContentSafetyResponse(
        hate_severity=1,
        self_harm_severity=3, # High self-harm
        sexual_severity=0,
        violence_severity=1
    )

    # Example thresholds
    my_thresholds = {
        "Hate": 3,
        "SelfHarm": 2, # Self-harm severity 2 or higher is not allowed
        "Sexual": 3,
        "Violence": 3
    }

    allowed_safe = safety_threshold(example_safe_result, my_thresholds)
    print(f"Is safe text allowed: {allowed_safe}") # Expected: True

    allowed_unsafe = safety_threshold(example_unsafe_result, my_thresholds)
    print(f"Is unsafe text allowed: {allowed_unsafe}") # Expected: False
