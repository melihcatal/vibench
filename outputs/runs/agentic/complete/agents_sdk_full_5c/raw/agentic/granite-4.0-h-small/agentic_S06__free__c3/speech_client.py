# speech_client.py
# [HELPER]
# Centralized Google Cloud Text-to-Speech client wrapper with configuration handling.

import os
from google.cloud import texttospeech

class TextToSpeechClient:
    """Purpose-built client for Text-to-Speech service.
    Automatically picks up credentials via GOOGLE_APPLICATION_CREDENTIALS.
    """
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, synthesis_input, voice, audio_config):
        """Delegate to the underlying client.
        Args:
            synthesis_input: texttospeech.SynthesisInput instance.
            voice: texttospeech.VoiceSelectionParams instance.
            audio_config: texttospeech.AudioConfig instance.
        Returns:
            texttospeech.SynthesizeSpeechResponse instance.
        """
        return self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

    def list_voices(self, language_code: str = "en-US"):
        """List voices for a given language.
        Returns: List of texttospeech.Voice instances.
        """
        return self.client.list_voices(language_code=language_code).voices
