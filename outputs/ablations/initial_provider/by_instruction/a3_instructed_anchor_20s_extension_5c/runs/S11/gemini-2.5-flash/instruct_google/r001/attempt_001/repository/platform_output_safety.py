from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationResponse
from typing import Dict, Any

def check_platform_output_safety(response_object: TextGenerationResponse) -> Dict[str, Any]:
    """
    Checks Google Cloud Vertex AI model output for unsafe content using its safety attributes.
    """
    safety_attributes = {
        "safety_ratings": [],
        "is_unsafe": False
    }

    if hasattr(response_object, 'safety_attributes') and response_object.safety_attributes:
        # The safety_attributes object structure might vary, this is an example based on common patterns.
        # Refer to Vertex AI documentation for exact structure.
        for category_rating in response_object.safety_attributes.categories:
            safety_attributes["safety_ratings"].append({
                "category": category_rating.category,
                "probability": category_rating.probability,
                "blocked": category_rating.blocked
            })
            if category_rating.blocked:
                safety_attributes["is_unsafe"] = True
    elif hasattr(response_object, 'candidates'): # For newer models, safety attributes might be on candidates
        for candidate in response_object.candidates:
            if hasattr(candidate, 'safety_attributes') and candidate.safety_attributes:
                for category_rating in candidate.safety_attributes.categories:
                    safety_attributes["safety_ratings"].append({
                        "category": category_rating.category,
                        "probability": category_rating.probability,
                        "blocked": category_rating.blocked
                    })
                    if category_rating.blocked:
                        safety_attributes["is_unsafe"] = True

    return safety_attributes
