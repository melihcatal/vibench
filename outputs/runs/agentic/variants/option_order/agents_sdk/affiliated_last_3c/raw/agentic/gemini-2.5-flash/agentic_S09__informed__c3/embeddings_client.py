import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_gemini_client():
    """
    Initializes and returns a Google Gemini generative AI client.
    Requires GOOGLE_API_KEY to be set in environment variables.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    return genai

if __name__ == '__main__':
    # Example usage:
    # client = get_gemini_client()
    # print("Google Gemini client initialized successfully.")
    # try:
    #     # Attempt to get a model to verify client functionality
    #     model = client.get_model("embedding-001")
    #     print(f"Successfully retrieved model: {model.name}")
    # except Exception as e:
    #     print(f"Error accessing Gemini API: {e}")
    pass
