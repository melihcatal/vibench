import os
from typing import List, Dict, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from model_models import (
    SafetyCheckRequest,
    SafetyCheckResponse,
    LLMRequest,
    LLMResponse,
)
from model_client import GeminiClient  # Reusing client to leverage safety settings


def check_prompt_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    # Configure safety settings based on the request threshold
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold[request.threshold],
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold[request.threshold],
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold[
            request.threshold
        ],
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold[
            request.threshold
        ],
    }

    # Although not a direct 'check' API, we can infer safety by attempting a generation
    # and checking the prompt_feedback. If it's blocked, it's unsafe.
    client = GeminiClient()
    # Temporarily override safety settings for this specific check, or pass them directly
    # A more robust solution might involve a dedicated safety endpoint if available
    try:
        # We need to create a new model instance or pass safety_settings to generate_text
        # For simplicity, we'll demonstrate how it would be used if `generate_text` accepted safety_settings
        model = genai.GenerativeModel(
            model_name="gemini-pro", safety_settings=safety_settings
        )
        response = model.generate_content(request.text)

        is_safe = (
            not response.prompt_feedback.block_reason
        )  # If there's no block reason, it's considered safe for the given threshold
        safety_ratings = [r.to_dict() for r in response.prompt_feedback.safety_ratings]

        return SafetyCheckResponse(is_safe=is_safe, safety_ratings=safety_ratings)
    except Exception as e:
        # If an error occurs (e.g., content is blocked at a very low threshold before response object is fully formed),
        # we can assume it's unsafe or handle the specific error.
        # For the purpose of this example, a blocked generation is the main indicator.
        return SafetyCheckResponse(
            is_safe=False,
            safety_ratings=[
                {"category": "UNKNOWN", "probability": "HIGH", "message": str(e)}
            ],
        )
