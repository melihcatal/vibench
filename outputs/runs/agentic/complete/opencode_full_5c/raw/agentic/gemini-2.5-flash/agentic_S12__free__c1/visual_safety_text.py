import google.generativeai as genai
from typing import List, Dict, Any


def check_text_safety(text_to_check: str) -> Dict[str, Any]:
    """Checks generated visual labels and descriptions for unsafe text using Google Cloud Generative AI.

    Args:
        text_to_check: The text string to check for safety.

    Returns:
        A dictionary indicating safety attributes and scores.
    """
    # Provider: Google Cloud Generative AI
    model = genai.GenerativeModel("gemini-pro")

    # The safety settings are defined to flag potentially harmful content.
    # Adjust thresholds as per application requirements.
    response = model.generate_content(
        f"Analyze the following text for safety and provide a safety report: {text_to_check}",
        safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ],
    )

    # Extract safety feedback from the response
    safety_feedback = {}
    if hasattr(response, "prompt_feedback") and hasattr(
        response.prompt_feedback, "safety_ratings"
    ):
        for rating in response.prompt_feedback.safety_ratings:
            safety_feedback[rating.category.name] = rating.probability.name

    # If the response was blocked, it might not have text content, handle it gracefully
    if not response.text:
        safety_feedback["moderation_status"] = "BLOCKED"
    else:
        safety_feedback["moderation_status"] = "PASSED"
        safety_feedback["model_output"] = (
            response.text
        )  # Model might provide an explanation

    return safety_feedback
