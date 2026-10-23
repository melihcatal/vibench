from messaging_client import get_gemini_model
import google.generativeai as genai


def check_message_safety(payload_text: str) -> dict:
    """Checks message payload text for unsafe content using Google Gemini Pro's safety features."""
    model = get_gemini_model("gemini-pro")

    # Gemini API has built-in safety settings. We just need to analyze the content.
    response = model.generate_content(
        payload_text,
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

    # The response object will contain a `prompt_feedback` attribute if safety limits were hit
    # or if there was other feedback (e.g., block reason).
    # If the response is blocked, response.text might not exist.
    safety_attributes = {
        "is_safe": True,  # Assume safe unless feedback indicates otherwise
        "safety_ratings": [],
    }

    if hasattr(response, "prompt_feedback") and response.prompt_feedback.safety_ratings:
        safety_attributes["is_safe"] = False
        for rating in response.prompt_feedback.safety_ratings:
            safety_attributes["safety_ratings"].append(
                {
                    "category": rating.category.name,
                    "probability": rating.probability.name,
                    "blocked": rating.blocked,
                }
            )

    # If the text was blocked and response.text is not available, indicate that.
    if not response.parts:
        safety_attributes["is_safe"] = False

    return safety_attributes
