import os
import google.generativeai as genai

def check_safety(text: str):
    """
    Checks the given text for unsafe content using Google's Generative AI.

    Args:
        text: The text content to check for safety.

    Returns:
        A dictionary indicating if the content is safe and any safety ratings.
    """
    # Configure the API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    safety_settings = [
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

    try:
        response = model.generate_content(
            text,
            safety_settings=safety_settings
        )

        if response._chunks:
            # If there are chunks, it means the content was blocked.
            # The actual safety feedback is in the prompt_feedback.
            return {
                "is_safe": False,
                "safety_ratings": [
                    {"category": rating.category.name, "probability": rating.probability.name, "blocked": rating.blocked}
                    for rating in response.prompt_feedback.safety_ratings
                ]
            }
        else:
            return {
                "is_safe": True,
                "safety_ratings": [
                    {"category": rating.category.name, "probability": rating.probability.name, "blocked": rating.blocked}
                    for rating in response.prompt_feedback.safety_ratings
                ]
            }

    except Exception as e:
        # Handle cases where the content is blocked before full generation
        # or other API errors.
        return {
            "is_safe": False,
            "error": str(e)
        }
