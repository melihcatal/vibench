import os

def apply_safety_thresholds(moderation_result: dict, thresholds: dict = None) -> dict:
    """
    Applies category thresholds to decide whether to allow text based on moderation results.
    This function expects moderation results structured similar to Google Cloud AI Platform's
    safety attributes for generative models.

    Args:
        moderation_result: A dictionary containing moderation outcomes, typically with
                           a 'safety_attributes' key. For Google Cloud generative models,
                           this might include categories like 'HARM_CATEGORY_TOXICITY',
                           'HARM_CATEGORY_VIOLENCE', etc., with associated scores.
        thresholds: A dictionary defining custom thresholds for different safety categories.
                    Keys are category names (e.g., 'TOXICITY'), values are float thresholds.

    Returns:
        A dictionary indicating whether the content is allowed and why (if not).
    """
    # Default thresholds for common Google Cloud AI Platform safety categories
    # These are illustrative and should be tuned based on policy.
    default_thresholds = {
        "HARM_CATEGORY_UNSPECIFIED": 0.5,
        "HARM_CATEGORY_TOXICITY": 0.7,
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": 0.8,
        "HARM_CATEGORY_DANGEROUS": 0.6,
        "HARM_CATEGORY_HATE_SPEECH": 0.75,
        "HARM_CATEGORY_HARASSMENT": 0.7,
    }

    if thresholds is None:
        thresholds = default_thresholds

    is_allowed = True
    reasons_for_denial = []

    # Assuming moderation_result contains 'safety_attributes' from a Google Cloud model
    # which would typically have a list of categories with scores and severities.
    # For this example, we'll simulate the structure based on common GenAI safety outputs.
    # In a real scenario, you'd parse the exact structure provided by `model.predict` or a dedicated safety API.

    # Placeholder for actual safety scores from a generative model output
    # In a real scenario, this would come from `moderation_result["moderation_result"]`
    # and would have detailed category scores.
    simulated_safety_scores = moderation_result.get("moderation_result", {})

    # Example of how you might check category scores if they were present
    # For now, we will use a simplified check based on a 'flagged' status from 'moderate_text.py'
    # If the moderation_result indicates any flagging, we can assume it's not allowed.
    if not simulated_safety_scores.get("checked", False):
        # If the moderation itself didn't run or return meaningful data, it's not allowed as a safety measure.
        is_allowed = False
        reasons_for_denial.append("Moderation check inconclusive or not performed.")
    elif simulated_safety_scores.get("flagged_category", None):
        # Simulate a scenario where `moderate_text` might flag a specific category implicitly
        # This would be replaced by actual score comparison from a real API response.
        flagged_category = simulated_safety_scores["flagged_category"].upper()
        # Check if the flagged category is above its threshold (simulated)
        if flagged_category in thresholds and simulated_safety_scores.get(flagged_category, 0.0) >= thresholds[flagged_category]:
             is_allowed = False
             reasons_for_denial.append(f"Content flagged for {flagged_category} above threshold ({thresholds[flagged_category]}).")
    elif simulated_safety_scores.get("some_score", 0.0) > 0.7: # Another generic simulation
        # This is a very generic placeholder. In a real scenario, you'd iterate through actual
        # safety attributes like `harm_category_scores` or similar fields from the model response.
        is_allowed = False
        reasons_for_denial.append("Generic high safety score detected.")

    # To make it concrete for Google Cloud, let's assume the moderation_result has a structure like:
    # {"moderation_result": {"checked": True, "HARM_CATEGORY_TOXICITY": 0.8, "HARM_CATEGORY_HATE_SPEECH": 0.3, ...}}
    # We'll adjust the simulation slightly for a more direct comparison.
    for category, score in moderation_result.get("moderation_result", {}).items():
        if isinstance(score, (int, float)) and category.startswith("HARM_CATEGORY_"):
            threshold_key = category # Directly use the full category name as key
            if score >= thresholds.get(threshold_key, 1.0): # Default to 1.0 (never block) if category not in thresholds
                is_allowed = False
                reasons_for_denial.append(f"Content scored {score:.2f} for {category}, exceeding threshold {thresholds.get(threshold_key, 1.0)}.")

    if not reasons_for_denial and not is_allowed: # Catch-all if logic didn't explicitly set a reason
         is_allowed = True # If no specific reason to deny, allow it.

    return {
        "original_result": moderation_result,
        "is_allowed": is_allowed,
        "reasons_for_denial": reasons_for_denial,
        "source": "Local thresholding with Google Cloud AI Platform expected output"
    }

if __name__ == "__main__":
    # Example usage with a simulated moderation result from Google Cloud AI Platform
    # In a real app, this would come from `moderate_text.py` or `moderate_batch.py`
    safe_content_result = {
        "text": "This is a nice message.",
        "moderation_result": {
            "checked": True,
            "HARM_CATEGORY_TOXICITY": 0.1,
            "HARM_CATEGORY_HATE_SPEECH": 0.05,
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": 0.01,
        }
    }
    decision = apply_safety_thresholds(safe_content_result)
    print(f"Decision for safe content: {decision}")

    unsafe_content_result = {
        "text": "I will harm you and your family!",
        "moderation_result": {
            "checked": True,
            "HARM_CATEGORY_TOXICITY": 0.9,
            "HARM_CATEGORY_HATE_SPEECH": 0.8,
            "HARM_CATEGORY_DANGEROUS": 0.95,
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": 0.1,
        }
    }
    decision = apply_safety_thresholds(unsafe_content_result)
    print(f"Decision for unsafe content: {decision}")

    custom_thresholds = {
        "HARM_CATEGORY_TOXICITY": 0.6,
        "HARM_CATEGORY_HATE_SPEECH": 0.5,
    }
    moderately_unsafe_content = {
        "text": "You are such a loser.",
        "moderation_result": {
            "checked": True,
            "HARM_CATEGORY_TOXICITY": 0.65,
            "HARM_CATEGORY_HATE_SPEECH": 0.4,
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": 0.05,
        }
    }
    decision_custom = apply_safety_thresholds(moderately_unsafe_content, custom_thresholds)
    print(f"Decision for moderately unsafe content with custom thresholds: {decision_custom}")
