from typing import Dict, Any, Optional
from google.cloud import aiplatform
# For specific harm categories and probabilities, these usually come in the response objects
# or are defined in the SDK if using a higher-level client.
# For raw API responses, they are often strings like 'HARM_CATEGORY_DANGEROUS_CONTENT' and 'PROBABILITY_HIGH'.

# Define common harm categories for convenience, matching Vertex AI's common responses
# These are often part of google.cloud.aiplatform_v1beta1.types.SafetyRating if using generated client types
# For simplicity, we define them as strings here, matching expected API output.

HARM_CATEGORIES = [
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
]

HARM_PROBABILITIES = {
    "HARM_PROBABILITY_UNSPECIFIED": 0,
    "NEGLIGIBLE": 0.1,
    "LOW": 0.3,
    "MEDIUM": 0.6,
    "HIGH": 0.9,
    "VERY_HIGH": 0.95, # Custom addition for potential very high values
}

def check_platform_output_safety(safety_attributes: Optional[Dict[str, Any]], threshold_probability: str = "MEDIUM") -> Dict[str, Any]:
    """Checks platform model output for unsafe content based on Vertex AI safety attributes.

    Args:
        safety_attributes: A dictionary containing safety attributes from the model response.
                           Expected format: {'categories': ['HARM_CATEGORY_...'], 'scores': ['PROBABILITY_...']}
        threshold_probability: The minimum harm probability level to flag as unsafe (e.g., 'MEDIUM', 'HIGH').

    Returns:
        A dictionary indicating if unsafe content was detected and details.
    """
    results = {
        "is_unsafe": False,
        "unsafe_categories": [],
        "details": safety_attributes
    }

    if not safety_attributes or not isinstance(safety_attributes, dict):
        return results

    categories = safety_attributes.get('categories', [])
    probabilities = safety_attributes.get('scores', [])

    threshold_value = HARM_PROBABILITIES.get(threshold_probability.upper(), 0.5) # Default to 0.5 if not found

    for i, category in enumerate(categories):
        if i < len(probabilities):
            probability_str = probabilities[i]
            probability_value = HARM_PROBABILITIES.get(probability_str.upper(), 0.0)
            
            if probability_value >= threshold_value:
                results["is_unsafe"] = True
                results["unsafe_categories"].append(f"{category} (Probability: {probability_str})")
    
    return results

if __name__ == '__main__':
    # Example usage with mock safety attributes from a Vertex AI response
    mock_safety_attributes_safe = {
        "categories": ["HARM_CATEGORY_DANGEROUS_CONTENT", "HARM_CATEGORY_HATE_SPEECH"],
        "scores": ["NEGLIGIBLE", "LOW"]
    }
    mock_safety_attributes_unsafe = {
        "categories": ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_SEXUALLY_EXPLICIT"],
        "scores": ["MEDIUM", "HIGH"]
    }
    mock_safety_attributes_empty = {}
    mock_safety_attributes_none = None

    print("--- Checking Safe Output ---")
    safety_check_safe = check_platform_output_safety(mock_safety_attributes_safe, threshold_probability="MEDIUM")
    print(safety_check_safe)

    print("\n--- Checking Unsafe Output (MEDIUM threshold) ---")
    safety_check_unsafe_medium = check_platform_output_safety(mock_safety_attributes_unsafe, threshold_probability="MEDIUM")
    print(safety_check_unsafe_medium)

    print("\n--- Checking Unsafe Output (HIGH threshold) ---")
    safety_check_unsafe_high = check_platform_output_safety(mock_safety_attributes_unsafe, threshold_probability="HIGH")
    print(safety_check_unsafe_high) # Only SEXUALLY_EXPLICIT should be flagged

    print("\n--- Checking Empty Attributes ---")
    safety_check_empty = check_platform_output_safety(mock_safety_attributes_empty)
    print(safety_check_empty)

    print("\n--- Checking None Attributes ---")
    safety_check_none = check_platform_output_safety(mock_safety_attributes_none)
    print(safety_check_none)

    # To make this fully integrated, you would pass the safety attributes from a Vertex AI model response
    # For example, from the `collect_platform_metadata.py` output's `raw_response` or `candidates[0].safety_attributes`
