import google.generativeai as genai
import os

def check_unsafe_content(text: str) -> dict:
    """
    Checks message payload text for unsafe content using Google's generative AI model.

    Args:
        text: The text content to check.

    Returns:
        A dictionary indicating if the content is safe and any safety ratings.
    """
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return {"error": "GOOGLE_API_KEY environment variable not set."}

    model = genai.GenerativeModel('gemini-pro')

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    try:
        response = model.generate_content(
            text,
            safety_settings=safety_settings
        )
        
        if not response._result.prompt_feedback.safety_ratings:
            return {"is_safe": True, "safety_ratings": []}

        for rating in response._result.prompt_feedback.safety_ratings:
            if rating.blocked:
                return {"is_safe": False, "safety_ratings": [str(rating)]}
        return {"is_safe": True, "safety_ratings": [str(r) for r in response._result.prompt_feedback.safety_ratings]}

    except Exception as e:
        return {"error": f"An error occurred: {e}"}

