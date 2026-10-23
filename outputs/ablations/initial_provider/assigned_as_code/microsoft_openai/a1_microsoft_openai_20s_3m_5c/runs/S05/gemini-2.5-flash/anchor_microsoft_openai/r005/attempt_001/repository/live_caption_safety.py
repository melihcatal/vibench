import google.generativeai as genai
import os

def check_content_safety(text: str) -> dict:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(
            text,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
            stream=False # Not streaming the response for a simple safety check
        )
        
        # If the prompt was blocked, response.prompt_feedback will contain the reason
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            return {
                "is_safe": False,
                "safety_ratings": [{'category': r.category.name, 'probability': r.probability.name} for r in response.prompt_feedback.safety_ratings]
            }
        
        # If not blocked, it's considered safe for the defined thresholds
        return {"is_safe": True, "safety_ratings": []}

    except Exception as e:
        # Handle cases where the API call itself fails or other errors occur
        print(f"Error checking content safety: {e}")
        return {"is_safe": False, "error": str(e)}

