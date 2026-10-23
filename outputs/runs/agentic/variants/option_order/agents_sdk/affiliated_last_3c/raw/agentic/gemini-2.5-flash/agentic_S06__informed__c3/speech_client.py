
import os
from google.cloud import texttospeech
from google.cloud import translate_v3 as translate
from google.cloud import speech_v1p1beta1 as speech
import google.generativeai as genai

class TextToSpeechClient:
    """Provides a configured Google Cloud Text-to-Speech client."""
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

class TranslationClient:
    """Provides a configured Google Cloud Translation client."""
    def __init__(self):
        self.client = translate.TranslationServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

class SpeechToTextClient:
    """Provides a configured Google Cloud Speech-to-Text client."""
    def __init__(self):
        self.client = speech.SpeechClient()

class GeminiEmbeddingClient:
    """Provides a configured Google Gemini Embedding client."""
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set for Gemini.")
        genai.configure(api_key=api_key)
        self.model = "models/embedding-001"
