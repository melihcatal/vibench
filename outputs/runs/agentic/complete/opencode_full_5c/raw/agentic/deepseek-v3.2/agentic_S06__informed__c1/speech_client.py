import os
from google.cloud import texttospeech
from typing import Optional, Dict, Any


class SpeechClient:
    """Configuration and client helper utilities for Text-to-Speech."""

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize Google Cloud TTS client.

        Args:
            credentials_path: Path to Google Cloud credentials JSON file.
                If None, uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.client = texttospeech.TextToSpeechClient()

    def get_default_audio_config(
        self, encoding: str = "MP3"
    ) -> texttospeech.AudioConfig:
        """Get default audio configuration."""
        encoding_map = {
            "MP3": texttospeech.AudioEncoding.MP3,
            "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
            "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
        }

        return texttospeech.AudioConfig(
            audio_encoding=encoding_map.get(encoding, texttospeech.AudioEncoding.MP3)
        )

    def create_voice_params(
        self,
        language_code: str = "en-US",
        voice_name: Optional[str] = None,
        gender: str = "NEUTRAL",
    ) -> texttospeech.VoiceSelectionParams:
        """Create voice selection parameters."""
        gender_map = {
            "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL,
            "MALE": texttospeech.SsmlVoiceGender.MALE,
            "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
        }

        return texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name if voice_name else "",
            ssml_gender=gender_map.get(gender, texttospeech.SsmlVoiceGender.NEUTRAL),
        )

    def synthesize(
        self,
        text: str,
        language_code: str = "en-US",
        voice_name: Optional[str] = None,
        encoding: str = "MP3",
    ) -> bytes:
        """Synthesize text to speech."""
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = self.create_voice_params(language_code, voice_name)
        audio_config = self.get_default_audio_config(encoding)

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return response.audio_content
