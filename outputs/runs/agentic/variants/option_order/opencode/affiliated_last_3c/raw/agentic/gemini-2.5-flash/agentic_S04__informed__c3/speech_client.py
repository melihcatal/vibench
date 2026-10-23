import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v3 as translate
from google.cloud import aiplatform
import google.generativeai as genai


class SpeechClient:
    def __init__(self):
        self.speech_client = speech.SpeechClient()
        self.translate_client = translate.TranslationServiceClient()
        self.perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.gemini_model = genai.GenerativeModel("gemini-pro")
        self.gemini_embedding_model = "models/embedding-001"


speech_client = SpeechClient()
