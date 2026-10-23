from google.generativeai.types import HarmCategory, SafetySetting

def check_platform_output_safety(model_output: str, safety_ratings: list) -> dict:
    """
    Checks platform model output for unsafe content based on provided safety ratings.

    Args:
        model_output: The text output from the platform model.
        safety_ratings: A list of dictionaries, where each dictionary represents a safety rating
                        and contains 'category' (HarmCategory enum) and 'probability' (str, e.g., 'HIGH', 'MEDIUM', etc.).

    Returns:
        A dictionary indicating if the content is safe and any detected harm categories.
    """
    unsafe_categories = []
    is_safe = True

    for rating in safety_ratings:
        category = rating.get('category')
        probability = rating.get('probability')

        if category and probability:
            # This is a simplified check. In a real scenario, you might compare probability
            # against a specific threshold (e.g., using SafetySetting.HarmBlockThreshold).
            # For demonstration, we'll consider 'HIGH' or 'MEDIUM' probability as unsafe.
            if probability in ['HIGH', 'MEDIUM']:
                is_safe = False
                # Ensure category is converted to a string for consistent output,
                # as HarmCategory is an enum.
                unsafe_categories.append(str(category))

    return {
        "is_safe": is_safe,
        "unsafe_categories": unsafe_categories,
        "original_output": model_output
    }
