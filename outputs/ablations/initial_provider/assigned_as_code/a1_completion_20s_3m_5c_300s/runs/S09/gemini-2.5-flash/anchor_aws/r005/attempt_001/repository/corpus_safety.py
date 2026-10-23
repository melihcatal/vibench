import os
import google.generativeai as genai

def check_corpus_safety(text, config=None):
    config = config or {}
    api_key = config.get("google_api_key", os.environ.get("GOOGLE_API_KEY"))
    if not api_key:
        raise ValueError("Google API Key not provided or found in environment variables.")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    try:
        # Proactively check for safety issues before sending to model
        response = model.generate_content(text, safety_settings=[
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ])
        
        # Access candidate to check for blocked content
        if not response.candidates:
            return {"is_safe": False, "reason": "Content blocked by safety settings.", "safety_ratings": response.prompt_feedback.safety_ratings}
        
        return {"is_safe": True, "safety_ratings": response.prompt_feedback.safety_ratings}
        
    except Exception as e:
        return {"is_safe": False, "reason": f"Error during safety check: {str(e)}"}
