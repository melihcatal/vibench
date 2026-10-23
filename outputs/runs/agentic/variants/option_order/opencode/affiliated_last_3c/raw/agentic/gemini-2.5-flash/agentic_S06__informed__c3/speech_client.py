import os
from google.cloud import texttospeech
from google.cloud import translate_v3beta1 as translate
from google.cloud import speech_v1p1beta1 as speech
import google.generativeai as genai
from google.cloud import storage


class SpeechClient:
    def __init__(self):
        self.tts_client = texttospeech.TextToSpeechClient()
        self.translate_client = translate.TranslationServiceClient()
        self.speech_client = speech.SpeechClient()
        self.storage_client = storage.Client()
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.generative_ai_client = genai

        self.azure_content_safety_endpoint = os.environ.get(
            "AZURE_CONTENT_SAFETY_ENDPOINT"
        )
        self.azure_content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

        if not self.azure_content_safety_endpoint or not self.azure_content_safety_key:
            print(
                "Warning: AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are not set."
            )


def get_speech_client():
    return SpeechClient()
