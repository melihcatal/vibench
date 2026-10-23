import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def check_corpus_safety(text: str):
    """
    Checks the safety attributes of the given text using Google's Gemini API.

    Args:
        text: The text string to check for safety.

    Returns:
        A dictionary containing the safety attributes of the text.
    """
    # Use a concrete third-party managed service: Google's Gemini API
    # The API key is assumed to be set up in the environment or initialized elsewhere.
    # For a real application, consider more robust authentication methods.
    
    # Provider-identifying signal: specific model ID
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        text,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    
    safety_attributes = {}
    if hasattr(response, 'prompt_feedback') and hasattr(response.prompt_feedback, 'safety_ratings'):
        for rating in response.prompt_feedback.safety_ratings:
            safety_attributes[rating.category.name] = rating.probability.name
    
    return safety_attributes
