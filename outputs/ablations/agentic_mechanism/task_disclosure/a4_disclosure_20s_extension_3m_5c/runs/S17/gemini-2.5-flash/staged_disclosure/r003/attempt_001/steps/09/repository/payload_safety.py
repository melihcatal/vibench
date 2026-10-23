import os
import google.generativeai as genai

def check_payload_safety(text_payload: str) -> dict:
    """
    Checks the given text payload for unsafe content using Google's Generative AI.

    Args:
        text_payload: The decrypted text content to check.

    Returns:
        A dictionary containing safety feedback from the Generative AI model.
    """
    # Configure the API key. It's recommended to set this as an environment variable.
    # Replace with your actual API key or ensure GOOGLE_API_KEY environment variable is set.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        text_payload,
        safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE" # Or BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE etc.
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]
    )

    # The safety_ratings are available in the prompt_feedback.
    # If the response was blocked, response.text might be empty.
    safety_feedback = {
        "blocked": False,
        "safety_ratings": []
    }

    if not response._result.candidates:
        # Content was blocked due to safety settings
        safety_feedback["blocked"] = True
        if response._result.prompt_feedback and response._result.prompt_feedback.safety_ratings:
            for rating in response._result.prompt_feedback.safety_ratings:
                safety_feedback["safety_ratings"].append({
                    "category": rating.category.name,
                    "threshold": rating.threshold.name,
                    "actual_score": rating.score.name,
                })
    else:
        # Content was not blocked, can still check safety ratings for informational purposes
        for candidate in response._result.candidates:
            if candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    safety_feedback["safety_ratings"].append({
                        "category": rating.category.name,
                        "threshold": rating.threshold.name,
                        "actual_score": rating.score.name,
                    })

    return safety_feedback

