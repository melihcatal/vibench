import os
from typing import Optional, Dict, Any
from google.cloud import aiplatform
from google.cloud.aiplatform.generative_models import GenerativeModel
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def moderate_text_safety(
    text_content: str,
    project_id: str,
    location: str,
    model_name: str = "gemini-pro",
) -> Dict[str, Any]:
    """Moderates text content for safety using Google Cloud Vertex AI generative models.
    Returns safety attributes and whether the content is blocked based on thresholds.
    """
    aiplatform.init(project=project_id, location=location)
    model = GenerativeModel(model_name)

    # Safety settings to configure blocking thresholds
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

    try:
        response = model.generate_content(
            contents=[text_content],
            safety_settings=safety_settings,
        )

        safety_attributes = {
            "blocked": False,
            "scores": {},
            "categories": {},
        }

        # Check if the response was blocked by safety settings
        if not response._result.candidates:
            safety_attributes["blocked"] = True
            safety_attributes["block_reason"] = "Content blocked by safety settings."
            return safety_attributes

        # Extract safety ratings
        for rating in response._result.prompt_feedback.safety_ratings:
            category_name = HarmCategory(rating.category).name.replace("HARM_CATEGORY_", "")
            safety_attributes["categories"][category_name] = rating.probability.name
            # If any category is BLOCKED, the overall content is considered blocked
            if rating.probability >= HarmBlockThreshold.BLOCK_LOW_AND_ABOVE:
                safety_attributes["blocked"] = True
                safety_attributes["block_reason"] = f"Blocked due to {category_name} with probability {rating.probability.name}."

        return safety_attributes

    except Exception as e:
        print(f"Error moderating text with Vertex AI: {e}")
        return {"blocked": False, "error": str(e), "scores": {}, "categories": {}}
