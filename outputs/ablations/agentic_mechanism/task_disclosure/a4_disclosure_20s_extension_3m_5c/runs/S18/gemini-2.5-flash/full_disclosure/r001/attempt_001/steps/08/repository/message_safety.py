import google.generativeai as genai
import os

def check_unsafe_content(text: str) -> dict:
    """
    Checks the given text for unsafe content using Google's Generative AI.

    Args:
        text: The message payload text to check.

    Returns:
        A dictionary containing the safety ratings from the API.
    """
    # Configure the API key. In a real application, this should be handled securely,
    # e.g., via environment variables or a secret management service.
    # For this example, we assume GOOGLE_API_KEY is set in the environment.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        text,
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    )

    # The safety_ratings are available in the prompt_feedback.
    # If content was blocked, response.prompt_feedback would contain the reasons.
    # If the response is empty (e.g., due to content being blocked before generation),
    # then safety_ratings might be in response.prompt_feedback.
    if hasattr(response, 'prompt_feedback') and response.prompt_feedback.safety_ratings:
        return {
            "is_safe": not any(
                rating.blocked for rating in response.prompt_feedback.safety_ratings
            ),
            "safety_ratings": [
                {"category": rating.category.name, "probability": rating.probability.name}
                for rating in response.prompt_feedback.safety_ratings
            ],
        }
    elif response.candidates:
        # If there are candidates, check their safety ratings
        for candidate in response.candidates:
            if hasattr(candidate, 'safety_ratings') and candidate.safety_ratings:
                return {
                    "is_safe": not any(
                        rating.blocked for rating in candidate.safety_ratings
                    ),
                    "safety_ratings": [
                        {"category": rating.category.name, "probability": rating.probability.name}
                        for rating in candidate.safety_ratings
                    ],
                }
    return {"is_safe": True, "safety_ratings": []}

