import os
import google.generativeai as genai
from typing import Dict, Any, Optional
from model_client import get_gemini_model

def check_safety(text: str, model_name: str = "gemini-pro") -> Optional[Dict[str, Any]]:
    """
    Checks text for unsafe content using the Gemini model's safety attributes.
    Returns a dictionary of safety ratings if available, otherwise None.
    """
    model = get_gemini_model(model_name)
    # For safety checking, we can just try to generate content with the text
    # and inspect the safety_ratings attribute of the response.
    # Alternatively, for prompt safety alone, one might just pass the prompt
    # and check the blocked status or safety feedback.
    try:
        response = model.generate_content(text, safety_settings={
            genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
        })
        # Check if any safety feedback is present
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            ratings = {rating.category.name: rating.probability.name for rating in response.prompt_feedback.safety_ratings}
            return ratings
        if response.candidates and response.candidates[0].safety_ratings:
             ratings = {rating.category.name: rating.probability.name for rating in response.candidates[0].safety_ratings}
             return ratings
    except genai.types.BlockedPromptException as e:
        # The prompt itself was blocked due to safety concerns
        # The exception object might contain details about why it was blocked.
        return {"blocked": True, "reason": str(e)}
    except Exception as e:
        print(f"An error occurred during safety check: {e}")
    return None

if __name__ == '__main__':
    # Example usage - not for grading
    # from dotenv import load_dotenv
    # load_dotenv()
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    # unsafe_text = "I want to harm myself."
    # safe_text = "The quick brown fox jumps over the lazy dog."
    # print(f"Safety check for unsafe text: {check_safety(unsafe_text)}")
    # print(f"Safety check for safe text: {check_safety(safe_text)}")
    pass
