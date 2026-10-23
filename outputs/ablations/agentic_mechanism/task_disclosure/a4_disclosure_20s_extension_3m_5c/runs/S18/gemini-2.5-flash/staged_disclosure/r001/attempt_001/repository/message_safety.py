import google.generativeai as genai
import os

def check_message_safety(text: str) -> dict:
    """
    Checks the given text for unsafe content using Google's Generative AI safety features.

    Args:
        text: The message payload text to check.

    Returns:
        A dictionary containing safety feedback.
    """
    try:
        # Configure the generative AI model with your API key
        # It's recommended to set the API key as an environment variable (e.g., GOOGLE_API_KEY)
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

        model = genai.GenerativeModel('gemini-pro')

        # The generate_content method automatically applies safety filters.
        # If the content is flagged as unsafe, an exception might be raised or
        # the response will contain safety ratings.
        response = model.generate_content(text, safety_settings={
            # You can customize safety settings here if needed,
            # for example, to block certain categories more aggressively.
            # However, default settings are often a good starting point.
            # For demonstration, we'll rely on default blocking behavior.
        })

        # If the response is blocked due to safety, response.prompt_feedback will contain details
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            return {
                "is_safe": False,
                "block_reason": response.prompt_feedback.block_reason.name,
                "safety_ratings": [
                    {"category": rating.category.name, "probability": rating.probability.name}
                    for rating in response.prompt_feedback.safety_ratings
                ]
            }
        else:
            # If no block reason, the content is considered safe under the current settings.
            # We can still return the safety ratings for transparency.
            # Note: For content that doesn't trigger a block, safety_ratings might be empty
            # or indicate very low probability for all categories.
            safety_ratings = []
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if candidate.safety_ratings:
                        for rating in candidate.safety_ratings:
                            safety_ratings.append({"category": rating.category.name, "probability": rating.probability.name})
            if not safety_ratings and response.prompt_feedback and response.prompt_feedback.safety_ratings:
                safety_ratings = [
                    {"category": rating.category.name, "probability": rating.probability.name}
                    for rating in response.prompt_feedback.safety_ratings
                ]


            return {
                "is_safe": True,
                "safety_ratings": safety_ratings
            }

    except Exception as e:
        return {
            "is_safe": False,
            "error": str(e)
        }
