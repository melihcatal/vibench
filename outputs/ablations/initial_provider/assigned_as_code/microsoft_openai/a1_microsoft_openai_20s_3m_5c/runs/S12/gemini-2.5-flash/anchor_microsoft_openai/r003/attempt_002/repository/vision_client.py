import os
import google.generativeai as genai
from google.cloud import vision_v1
from google.cloud import storage
from google.cloud import translate_v3 as translate

def get_vision_client():
    return vision_v1.ImageAnnotatorClient()

def get_storage_client():
    return storage.Client()

def get_translate_client():
    return translate.TranslationServiceClient()

def get_generative_model(model_name: str = "gemini-pro"):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)
