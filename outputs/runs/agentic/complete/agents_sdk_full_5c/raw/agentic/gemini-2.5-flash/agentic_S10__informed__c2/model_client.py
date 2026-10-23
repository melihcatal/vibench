import os
import google.generativeai as genai

# Configure the Gemini API with your API key
# GOOGLE_API_KEY environment variable should be set
if os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
else:
    print("Warning: GOOGLE_API_KEY environment variable not set. Gemini API calls may fail.")

def get_gemini_model(model_name: str):
    """Returns a generative model instance for the given model name."""
    return genai.GenerativeModel(model_name)
