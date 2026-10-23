import os
from typing import Dict, Any
import google.generativeai as genai

def check_text_safety(text_content: str) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using Google Cloud Generative AI.
    This implementation uses the model's built-in safety features.
    
    Args:
        text_content: The text content to check for safety.
        
    Returns:
        A dictionary indicating safety attributes. Returns model's safety ratings.
        An empty dict if an error occurs or API key is missing.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("GOOGLE_API_KEY environment variable not set.")
        return {}

    genai.configure(api_key=google_api_key)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        # Generating content to implicitly get safety ratings.
        # A more direct safety API might be preferred for production.
        # This demonstrates using the model for general content processing that includes safety checks.
        response = model.generate_content(
            f"Review the following text for safety compliance: {text_content}"
        )
        
        safety_ratings = []
        if response and response.prompt_feedback and response.prompt_feedback.safety_ratings:
            for rating in response.prompt_feedback.safety_ratings:
                safety_ratings.append({
                    "category": str(rating.category).split('.')[-1], # e.g., HARM_CATEGORY_HATE_SPEECH
                    "threshold": str(rating.threshold).split('.')[-1], # e.g., BLOCK_LOW_AND_ABOVE
                    "probability": str(rating.probability).split('.')[-1] # e.g., NEGLIGIBLE
                })
        
        return {"safety_ratings": safety_ratings}
        
    except Exception as e:
        print(f"Error checking text safety: {e}")
    return {}

if __name__ == "__main__":
    # Example Usage (requires GOOGLE_API_KEY)
    safe_text = "Hello, how are you today? This is a perfectly safe message."
    unsafe_text = "I hate you so much, you are the worst!"
    
    print("Checking safe text for safety...")
    safe_result = check_text_safety(safe_text)
    print("\nSafe Text Safety Check Result:", safe_result)

    print("\nChecking unsafe text for safety...")
    unsafe_result = check_text_safety(unsafe_text)
    print("\nUnsafe Text Safety Check Result:", unsafe_result)
