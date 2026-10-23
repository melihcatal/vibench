import os
from google.cloud import texttospeech_v1 as texttospeech


class GoogleTTSClient:
    """Generate spoken previews of translated copy using Google Cloud Text-to-Speech."""

    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text: str, language_code: str, voice_name: str = None) -> bytes:
        """Synthesize speech from text."""
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name if voice_name else f"{language_code}-Standard-A"
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return response.audio_content


def localized_audio_preview(text: str, language_code: str) -> bytes:
    """Generate spoken previews of translated copy using Google Cloud Text-to-Speech."""
    client = GoogleTTSClient()
    return client.synthesize_speech(text, language_code)