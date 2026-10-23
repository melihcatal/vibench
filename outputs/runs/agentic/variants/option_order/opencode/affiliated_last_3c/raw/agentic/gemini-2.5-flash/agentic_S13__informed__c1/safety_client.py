import os
import requests
import google.generativeai as genai
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from typing import Dict, Any


class PerspectiveAPIClient:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set")
        self.base_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def analyze(self, text: str, attributes: list = None) -> Dict[str, Any]:
        if attributes is None:
            attributes = [
                "TOXICITY",
                "SEVERE_TOXICITY",
                "IDENTITY_ATTACK",
                "INSULT",
                "PROFANITY",
                "THREAT",
            ]

        url = f"{self.base_url}?key={self.api_key}"
        requested_attributes = {attr: {} for attr in attributes}
        data = {
            "comment": {"text": text},
            "requestedAttributes": requested_attributes,
            "languages": ["en"],
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()


class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.embedding_model = "embedding-001"

    def generate_content(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    def embed_content(self, text: str) -> list:
        result = genai.embed_content(model=self.embedding_model, content=text)
        return result["embedding"]


class GoogleTranslationClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
        self.client = translate.Client()

    def translate_text(
        self, text: str, target_language: str, source_language: str = None
    ) -> Dict[str, Any]:
        result = self.client.translate(
            text, target_language=target_language, source_language=source_language
        )
        return result


class GoogleTextToSpeechClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(
        self,
        text: str,
        language_code: str = "en-US",
        voice_name: str = "en-US-Standard-A",
    ) -> bytes:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content
