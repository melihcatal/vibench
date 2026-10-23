from typing import Dict, Any
from model_models import InferenceResponse


def check_safety(response: InferenceResponse) -> Dict[str, Any]:
    """Checks generated text for unsafe content using Vertex AI's built-in safety attributes.

    This function relies on the safety ratings provided by the Vertex AI generative model (google.cloud.aiplatform).
    """
    safety_assessment = {"is_safe": True, "safety_details": []}

    if response.safety_attributes and "safety_ratings" in response.safety_attributes:
        for rating in response.safety_attributes["safety_ratings"]:
            category = rating.get("category")
            probability = rating.get("probability")
            blocked = rating.get("blocked", False)  # Vertex AI specific

            if blocked or (
                probability and probability in ["HIGH", "VERY_HIGH"]
            ):  # Customize threshold as needed
                safety_assessment["is_safe"] = False
                safety_assessment["safety_details"].append(
                    {
                        "category": category,
                        "probability": probability,
                        "blocked": blocked,
                        "message": f"Content detected in category '{category}' with probability '{probability}' (blocked: {blocked}).",
                    }
                )

    if not safety_assessment["is_safe"] and not safety_assessment["safety_details"]:
        safety_assessment["safety_details"].append(
            {
                "message": "Safety check performed, but no specific details provided by the model for the detected unsafety."
            }
        )

    return safety_assessment
