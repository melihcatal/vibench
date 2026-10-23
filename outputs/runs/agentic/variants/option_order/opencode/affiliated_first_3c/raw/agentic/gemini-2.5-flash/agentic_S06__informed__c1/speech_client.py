import os
from google.cloud import texttospeech
from google.cloud import translate_v3beta1 as translate
from google.cloud import speech_v1p1beta1 as speech
import google.generativeai as genai
import requests


class TextToSpeechClient:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()


class TranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")


class SpeechToTextClient:
    def __init__(self):
        self.client = speech.SpeechClient()


class GeminiEmbeddingClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.get_model("models/embedding-001")


class PerspectiveAPIClient:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        self.base_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )
