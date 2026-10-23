import os
from typing import Dict, Any
from google.cloud import aiplatform
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def moderate_vendor_text(text: str) -> Dict[str, Any]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID must be set in environment variables.")

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.GenerativeModel("gemini-pro") # Using gemini-pro for content moderation

    # Configure safety settings. Adjust thresholds as needed.
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    try:
        response = model.generate_content(text, safety_settings=safety_settings)
        # If the content is blocked, response.text will raise an exception.
        # Accessing `prompt_feedback` directly to check safety attributes.
        return {
            "original_text": text,
            "is_safe": not response._raw_response.prompt_feedback.block_reason,
            "safety_ratings": [{
                "category": rating.category.name,
                "probability": rating.probability.name,
                "blocked": rating.blocked
            } for rating in response._raw_response.prompt_feedback.safety_ratings]
        }
    except Exception as e:
        # This typically means the content was blocked, and response.text would fail.
        # We can still return safety ratings if available in the exception or raw response.
        return {
            "original_text": text,
            "is_safe": False, # Assuming unsafe if an exception occurred during generation due to safety.
            "error": str(e),
            "safety_ratings": [] # Placeholder, could try to parse from error if detailed.
        }
