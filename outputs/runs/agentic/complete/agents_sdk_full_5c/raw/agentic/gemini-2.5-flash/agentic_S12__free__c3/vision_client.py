import os
from google.cloud import vision
import google.generativeai as genai

def get_vision_client():
    """Returns a configured Google Cloud Vision API client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    return vision.ImageAnnotatorClient()

def get_gemini_pro_vision_model():
    """Returns a configured Google Generative AI (gemini-pro-vision) model."""
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    return genai.GenerativeModel('gemini-pro-vision')

def get_gemini_pro_model():
    """Returns a configured Google Generative AI (gemini-pro) model."""
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    return genai.GenerativeModel('gemini-pro')

# You can add more client configurations here as needed.

if __name__ == '__main__':
    # Example usage for demonstration
    print("Initializing Vision client...")
    try:
        vision_client = get_vision_client()
        print(f"Vision client created: {vision_client}")
    except Exception as e:
        print(f"Could not create Vision client: {e}")
        print("Ensure GOOGLE_APPLICATION_CREDENTIALS is set.")

    print("\nInitializing Gemini Pro Vision model...")
    try:
        gemini_vision_model = get_gemini_pro_vision_model()
        print(f"Gemini Pro Vision model created: {gemini_vision_model}")
    except Exception as e:
        print(f"Could not create Gemini Pro Vision model: {e}")
        print("Ensure GEMINI_API_KEY is set.")

    print("\nInitializing Gemini Pro model...")
    try:
        gemini_pro_model = get_gemini_pro_model()
        print(f"Gemini Pro model created: {gemini_pro_model}")
    except Exception as e:
        print(f"Could not create Gemini Pro model: {e}")
        print("Ensure GEMINI_API_KEY is set.")
