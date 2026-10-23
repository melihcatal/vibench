import os
from google.cloud import texttospeech
from google.cloud import translate_v3 as translate
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import google.generativeai as genai
from google.cloud import speech_v1p1beta1 as speech


def get_text_to_speech_client():
    # Google Cloud Text-to-Speech requires GOOGLE_APPLICATION_CREDENTIALS
    return texttospeech.TextToSpeechClient()


def get_translation_client():
    # Google Cloud Translation requires GOOGLE_APPLICATION_CREDENTIALS
    return translate.TranslationServiceClient()


def get_content_safety_client():
    # Azure AI Content Safety requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))


def get_embedding_model():
    # Gemini Embeddings requires GOOGLE_API_KEY
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.get_model("embedding-001")


def get_speech_to_text_client():
    # Google Cloud Speech-to-Text requires GOOGLE_APPLICATION_CREDENTIALS
    return speech.SpeechClient()
