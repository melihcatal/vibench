import os
from google.cloud import texttospeech


class TextToSpeechClientWrapper:
    """Local wrapper that initializes the provider client and provides helper methods."""

    def __init__(self):
        # Use environment variable or default path for credentials
        credentials_path = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS", "path/to/credentials.json"
        )
        self.client = texttospeech.TextToSpeechClient.from_service_account_json(
            credentials_path
        )

    def synthesize_text(
        self,
        text: str,
        voice_name: str = "en-US-Wavenet-D",
        audio_encoding: str = "MP3",
    ) -> bytes:
        """Synthesize plain text to audio."""
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name=voice_name
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return response.audio_content

    def synthesize_ssml(
        self,
        ssml: str,
        voice_name: str = "en-US-Wavenet-F",
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
        audio_encoding: str = "MP3",
    ) -> bytes:
        """Synthesize SSML with prosody controls."""
        input_text = texttospeech.SynthesisInput(ssml=ssml)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name=voice_name
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch,
        )
        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return response.audio_content
