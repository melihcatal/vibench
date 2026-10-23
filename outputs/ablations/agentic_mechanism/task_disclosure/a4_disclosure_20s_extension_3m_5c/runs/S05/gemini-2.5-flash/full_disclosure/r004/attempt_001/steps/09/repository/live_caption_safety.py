import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def check_safety(text: str):
    """
    Checks the given text for unsafe content using Google's Generative AI safety features.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        text,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )
    
    # If the response was blocked due to safety concerns, access the prompt_feedback.
    if not response._result.candidates:
        return {"flagged": True, "safety_ratings": response._result.prompt_feedback.safety_ratings}
    else:
        # If there are candidates, it means the content was not blocked
        # Still, we can return the safety ratings for informational purposes.
        # This part assumes we want to know the ratings even if not blocked.
        # The actual content of the response would be in response.text if needed.
        return {"flagged": False, "safety_ratings": response._result.prompt_feedback.safety_ratings}

