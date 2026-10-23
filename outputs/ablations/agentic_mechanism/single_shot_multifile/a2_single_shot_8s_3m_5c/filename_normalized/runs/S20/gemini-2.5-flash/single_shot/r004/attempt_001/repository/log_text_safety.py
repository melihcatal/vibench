import os
from typing import List
from observability_client import get_generative_model
from observability_models import SafetyCheckResult
import google.generativeai as genai

def check_log_text_safety(text: str) -> SafetyCheckResult:
    model = get_generative_model(model_name="gemini-pro")

    # The GenerativeModel's generate_content method inherently applies safety settings
    # We don't directly query safety settings, but rather check if the content would be blocked
    # or if safety feedback is provided in the response.
    
    # For a direct programmatic check of safety attributes, you'd typically send a request
    # to a specific moderation endpoint or rely on the LLM's built-in safety feedback.
    # Gemini API automatically performs safety filtering. If content is unsafe, the response
    # might be empty or indicate blockage.
    
    # A more explicit way to get safety attributes would be if the API exposed them directly
    # in a structured way for a given prompt, without necessarily blocking generation.
    # For this example, we'll simulate by checking if content is blocked or if safety_ratings exist.

    try:
        response = model.generate_content(text, safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ])

        safety_feedback = response.prompt_feedback.safety_ratings if response.prompt_feedback else []

        flagged = any(rating.blocked for rating in safety_feedback) if safety_feedback else False
        categories = {rating.category.split('_')[-1].lower(): rating.blocked for rating in safety_feedback} if safety_feedback else {}
        scores = {rating.category.split('_')[-1].lower(): float(rating.probability) for rating in safety_feedback} if safety_feedback else {}

        return SafetyCheckResult(flagged=flagged, categories=categories, score=scores)

    except genai.types.BlockedPromptException as e:
        # This exception is raised if the prompt itself is blocked by safety settings
        # We can infer it's flagged and try to extract categories if available from the exception or defaults.
        # The specific details in BlockedPromptException might vary.
        print(f"Warning: Prompt blocked by safety settings: {e}")
        # Defaulting to true for flagged if the prompt is blocked
        return SafetyCheckResult(flagged=True, categories={}, score={})
    except Exception as e:
        # Catch other potential errors from the API call
        print(f"Error during safety check: {e}")
        return SafetyCheckResult(flagged=False, categories={}, score={})

