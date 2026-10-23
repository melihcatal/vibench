import os

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def check_text_safety(text_content: str, project_id: str, location: str = "us-central1") -> dict:
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using gemini-pro for content moderation capabilities
    response = model.generate_content(
        text_content,
        safety_settings={
            vertexai.language_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: vertexai.language_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            vertexai.language_models.HarmCategory.HARM_CATEGORY_HARASSMENT: vertexai.language_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            vertexai.language_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: vertexai.language_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            vertexai.language_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: vertexai.language_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
    )

    # The safety attributes are usually in the candidates if the content is not blocked.
    # If content is blocked, an exception might be raised or no candidates returned.
    if response.candidates and hasattr(response.candidates[0], 'safety_ratings'):
        safety_attributes = {
            rating.category.name: rating.probability.name
            for rating in response.candidates[0].safety_ratings
        }
        return {"is_safe": True, "safety_attributes": safety_attributes}
    else:
        # If no candidates or it was blocked, consider it potentially unsafe or requiring review
        return {"is_safe": False, "message": "Content may be unsafe or was blocked."}
