import os
from google.cloud import texttospeech
from google.cloud import translate_v3 as translate
from google.cloud import speech_v1p1beta1 as speech
import google.generativeai as genai
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient


def get_tts_client():
    return texttospeech.TextToSpeechClient()


def get_translate_client():
    return translate.TranslationServiceClient()


def get_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))


def get_embedding_model():
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro")


def get_stt_client():
    return speech.SpeechClient()
