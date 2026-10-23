import os
import google.generativeai as genai

def check_safety(text: str):
    """
    Checks the given text for unsafe content using a hosted LLM.

    Args:
        text: The text to be checked.

    Returns:
        A dictionary containing safety feedback, or an error message if the check fails.
    """
    try:
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(text, safety_settings=[
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        ])
        
        # Access safety feedback
        safety_feedback = {}
        if hasattr(response, 'prompt_feedback') and hasattr(response.prompt_feedback, 'safety_ratings'):
            for rating in response.prompt_feedback.safety_ratings:
                safety_feedback[rating.category] = rating.probability.name
        
        return safety_feedback
    except Exception as e:
        return {"error": str(e)}

