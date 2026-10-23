from google.cloud import translate_v3beta1
from google.cloud import language_v1
from google.cloud import texttospeech
import google.generativeai as genai
import os


def get_translation_client():
    return translate_v3beta1.TranslationServiceClient()


def get_language_client():
    return language_v1.LanguageServiceClient()


def get_text_to_speech_client():
    return texttospeech.TextToSpeechClient()


def get_generative_model_for_embedding():
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel("text-embedding-004")
