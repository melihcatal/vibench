import os
from google.cloud import translate_v3beta1 as translate
import google.generativeai as genai
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import texttospeech


def get_translate_client():
    """Returns a Google Cloud Translation client."""
    return translate.TranslationServiceClient()


def get_gemini_client():
    """Returns a Google Gemini client."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai


def get_content_safety_client():
    """Returns an Azure AI Content Safety client."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))


def get_text_to_speech_client():
    """Returns a Google Cloud Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()
