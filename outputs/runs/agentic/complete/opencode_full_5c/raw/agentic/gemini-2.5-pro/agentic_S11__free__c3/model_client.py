import os
import cohere
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
import google.generativeai as genai

_cohere_api_key = os.getenv("COHERE_API_KEY")
cohere_client = cohere.Client(_cohere_api_key)

_google_api_key = os.getenv("GOOGLE_API_KEY")
if _google_api_key:
    genai.configure(api_key=_google_api_key)


def get_cohere_client():
    return cohere_client


def get_google_generativeai_client():
    return genai


def get_google_translate_client():
    return translate.Client()


def get_google_tts_client():
    return texttospeech.TextToSpeechClient()
