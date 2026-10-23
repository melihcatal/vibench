import os
import google.generativeai as genai

def get_gemini_model(model_name: str = "gemini-pro") -> genai.GenerativeModel:
    """
    Initializes and returns a Google Gemini GenerativeModel client.
    Configures the API key from the GOOGLE_API_KEY environment variable.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please set your API key.")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

# This client can be extended for other Google Cloud services if needed,
# but for now, it focuses on Generative AI models.
