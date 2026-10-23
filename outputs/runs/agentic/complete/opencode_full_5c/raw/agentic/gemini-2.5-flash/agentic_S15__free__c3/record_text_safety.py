import os
import vertexai
from vertexai.preview.generative_models import (
    GenerativeModel,
    Part,
    Image,
    HarmCategory,
    HarmBlockThreshold,
)
from typing import Dict, Any


def check_text_safety(
    text_content: str, project_id: str, location: str = "us-central1"
) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using Google Cloud Vertex AI (Generative AI).
    Returns a dictionary of safety attributes and scores.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    # The safety settings are applied during content generation and are part of the response.
    # We'll simply ask the model to analyze the text, and the response object will contain safety attributes.
    response = model.generate_content(
        text_content,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
        },
    )

    safety_attributes = {}
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_attributes[rating.category.name] = {
                "score": rating.probability.name,
                "blocked": rating.blocked,
            }

    return safety_attributes
