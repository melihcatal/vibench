
from google.cloud import texttospeech_v1 as texttospeech
import os

class TextToSpeechClientHelper:
    """Provides a singleton-like helper for Google Cloud Text-to-Speech client."""
    _client = None

    @classmethod
    def get_client(cls) -> texttospeech.TextToSpeechClient:
        """Returns an initialized Google Cloud Text-to-Speech client."""
        if cls._client is None:
            cls._client = texttospeech.TextToSpeechClient()
        return cls._client

    @staticmethod
    def get_default_voice_params(voice_name: str = "en-US-Wavenet-D") -> texttospeech.VoiceSelectionParams:
        """Returns default voice selection parameters."""
        return texttospeech.VoiceSelectionParams(
            language_code=voice_name.split('-')[0] + '-' + voice_name.split('-')[1], # e.g., "en-US"
            name=voice_name,
        )

    @staticmethod
    def get_default_audio_config(audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3) -> texttospeech.AudioConfig:
        """Returns default audio configuration parameters."""
        return texttospeech.AudioConfig(
            audio_encoding=audio_encoding
        )

if __name__ == '__main__':
    client = TextToSpeechClientHelper.get_client()
    print(f"Google Cloud Text-to-Speech client initialized: {client}")
    voice_params = TextToSpeechClientHelper.get_default_voice_params()
    print(f"Default Voice Params: {voice_params.name}, {voice_params.language_code}")
