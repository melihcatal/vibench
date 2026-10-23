import google.generativeai as genai
import os

def get_gemini_model(model_name: str):
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)
    return model
