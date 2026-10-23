import os
from google.cloud import vision
import google.generativeai as genai

def get_vision_client():
    """Returns a Google Cloud Vision API client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return vision.ImageAnnotatorClient()

def get_gemini_vision_model():
    """Returns a Google Gemini Pro Vision generative model."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro-vision')

def get_gemini_pro_model():
    """Returns a Google Gemini Pro generative model for text tasks."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

if __name__ == '__main__':
    print("Vision Client Initialized:", get_vision_client() is not None)
    try:
        print("Gemini Vision Model Initialized:", get_gemini_vision_model() is not None)
    except ValueError as e:
        print(f"Gemini Vision Model initialization failed: {e}")
    try:
        print("Gemini Pro Model Initialized:", get_gemini_pro_model() is not None)
    except ValueError as e:
        print(f"Gemini Pro Model initialization failed: {e}")
