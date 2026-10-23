from google.cloud import vision_v1p3beta1 as vision
from google.cloud import translate_v3 as translate
from google.cloud import storage
import google.generativeai as genai
import os


def get_vision_client():
    return vision.ImageAnnotatorClient()


def get_translate_client():
    return translate.TranslationServiceClient()


def get_storage_client():
    return storage.Client()


def get_generative_model(model_name: str):
    # Assumes GOOGLE_API_KEY is set in environment for genai
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)
