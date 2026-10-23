import os
from typing import Dict, Any
from document_client import get_google_safety_model

def moderate_vendor_notes(text_to_moderate: str) -> Dict[str, Any]:
    """Moderates vendor notes or memo fields using Google Cloud Vertex AI with safety attributes.

    Args:
        text_to_moderate: The text from vendor notes or memo fields.

    Returns:
        A dictionary containing the safety attribute scores and the raw model response.
    """
    project_id = os.environ.get('GCP_PROJECT_ID')
    location = os.environ.get('GCP_LOCATION', 'us-central1')
    model_name = os.environ.get('GCP_SAFETY_MODEL', 'gemini-pro') # Using gemini-pro for safety checks

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    model = get_google_safety_model(project_id, location, model_name)

    response = model.generate_content(
        text_to_moderate,
        safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
    )

    safety_attributes = {"blocked": False, "scores": {}}

    # Check if the content was blocked
    if response.prompt_feedback and response.prompt_feedback.block_reason: # Check for a block reason
        safety_attributes["blocked"] = True
        safety_attributes["block_reason"] = response.prompt_feedback.block_reason.name

    # Extract safety ratings if available
    if response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'safety_ratings'):
                for rating in candidate.safety_ratings:
                    category = rating.category.name.replace("HARM_CATEGORY_", "").lower()
                    safety_attributes["scores"][category] = rating.probability.name

    return {
        "safety_attributes": safety_attributes,
        "raw_model_response": response.to_dict() if hasattr(response, 'to_dict') else str(response)
    }
