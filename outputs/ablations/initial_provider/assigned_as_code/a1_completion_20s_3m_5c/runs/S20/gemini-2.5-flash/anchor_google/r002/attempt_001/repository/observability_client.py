import os
from google.cloud import logging_v2
from google.cloud import translate_v3beta1 as translate
from google.cloud import language_v2 as language
import google.generativeai as genai


def get_logging_client(project_id: str) -> logging_v2.Client:
    return logging_v2.Client(project=project_id)

def get_translate_client(project_id: str):
    return translate.TranslationServiceClient()

def get_language_client() -> language.LanguageServiceClient:
    return language.LanguageServiceClient()

def get_generative_model(model_name: str):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)
