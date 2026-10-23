import os
from functools import lru_cache
from google.cloud import logging
from google.cloud import translate_v3 as translate
import google.generativeai as genai

@lru_cache(maxsize=1)
def get_logging_client():
    return logging.Client()

@lru_cache(maxsize=1)
def get_translation_client():
    return translate.TranslationServiceClient()

@lru_cache(maxsize=1)
def get_generative_model(model_name: str = "gemini-pro"):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for Generative AI.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

@lru_cache(maxsize=1)
def get_embedding_model(model_name: str = "embedding-001"):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for Generative AI.")
    genai.configure(api_key=api_key)
    return genai.get_model(model_name)
