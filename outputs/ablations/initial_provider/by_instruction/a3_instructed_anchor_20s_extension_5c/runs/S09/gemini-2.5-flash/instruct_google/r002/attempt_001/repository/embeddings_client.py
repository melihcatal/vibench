import os
import google.generativeai as genai

def get_gemini_client():
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai
