import os
from typing import List

from vertexai.preview.generative_models import (
    GenerationConfig,
    Part,
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
)

from document_client import GoogleCloudClients
from document_models import SafetyCheckResult, SafetyRating


def check_text_for_safety(text: str) -> SafetyCheckResult:
    """Checks extracted document text for unsafe content using Google Cloud Vertex AI (GenerativeModel).

    Args:
        text: The text content to check.

    Returns:
        A SafetyCheckResult object indicating if the content is safe and providing safety ratings.
    """
    model = GoogleCloudClients.get_vertex_ai_model_garden_client()

    # Configure safety settings for content generation
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

    # Sending the text as content to be processed by the model for safety attributes.
    # We are not asking it to generate new text, but to evaluate the input.
    # The response will contain safety_ratings which we can then interpret.
    try:
        response = model.generate_content(
            [text],
            safety_settings=safety_settings,
            generation_config=GenerationConfig(
                max_output_tokens=1
            ),  # Minimal output, just to trigger safety check
        )

        is_safe = True
        safety_ratings: List[SafetyRating] = []

        if (
            response._raw_response.prompt_feedback
            and response._raw_response.prompt_feedback.safety_ratings
        ):
            for rating in response._raw_response.prompt_feedback.safety_ratings:
                safety_ratings.append(
                    SafetyRating(
                        category=HarmCategory(
                            rating.category
                        ).name,  # Convert enum to string
                        probability=HarmBlockThreshold(
                            rating.block_threshold
                        ).name,  # Convert enum to string
                    )
                )
                if (
                    rating.blocked
                ):  # If any category is blocked, the content is not safe
                    is_safe = False

        return SafetyCheckResult(is_safe=is_safe, safety_ratings=safety_ratings)

    except Exception as e:
        # If the content is blocked before generation, an exception is raised.
        # This indicates the content is definitively unsafe.
        print(f"Content blocked by safety filters: {e}")
        return SafetyCheckResult(
            is_safe=False, safety_ratings=[]
        )  # No detailed ratings if blocked at input
