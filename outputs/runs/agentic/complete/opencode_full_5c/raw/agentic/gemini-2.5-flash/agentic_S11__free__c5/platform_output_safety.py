from typing import Dict, Any
from model_models import ModelResponse


def check_platform_output_safety(response: ModelResponse) -> Dict[str, Any]:
    """
    Checks the platform model output for unsafe content using provided safety attributes.
    Assumes safety_attributes is a dictionary from Vertex AI's response structure.
    """
    if response.safety_attributes:
        # Vertex AI safety attributes typically include categories and scores.
        # Example structure: {'categories': ['HARM_CATEGORY_TOXICITY'], 'scores': [0.8], 'blocked': False}
        # We'll return the raw safety attributes for detailed inspection.
        return {
            "has_unsafe_content": any(
                score > 0.7 for score in response.safety_attributes.get("scores", [])
            ),  # Example threshold
            "safety_details": response.safety_attributes,
            "original_text": response.text,
        }
    else:
        return {
            "has_unsafe_content": False,
            "safety_details": "No safety attributes provided.",
            "original_text": response.text,
        }
