import google.generativeai as genai
import os

def check_unsafe_content(text: str):
    """
    Checks the given text for unsafe content using Google's Generative AI safety features.

    Args:
        text: The document text to check.

    Returns:
        A dictionary containing safety attributes and scores.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        text,
        safety_settings={
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
        }
    )

    # The actual safety ratings are in the `prompt_feedback` attribute
    # if content was blocked or in `candidates[0].safety_ratings` otherwise.
    # For this function, we assume we want to get the safety attributes regardless of blocking.
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        return {
            rating.category.name: rating.probability.name
            for rating in response.prompt_feedback.safety_ratings
        }
    elif response.candidates and response.candidates[0].safety_ratings:
        return {
            rating.category.name: rating.probability.name
            for rating in response.candidates[0].safety_ratings
        }
    else:
        return {}
