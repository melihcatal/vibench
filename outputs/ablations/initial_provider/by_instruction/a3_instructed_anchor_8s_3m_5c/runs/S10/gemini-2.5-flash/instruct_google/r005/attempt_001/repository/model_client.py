import google.generativeai as genai
import os

def get_gemini_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=api_key)
    return genai

def get_generative_model(model_name: str):
    client = get_gemini_client()
    return client.GenerativeModel(model_name)
