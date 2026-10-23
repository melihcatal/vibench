# [HELPER] speech_client.py

# Uses Google Cloud Text-to-Speech SDK (provider identifier via import)
from google.cloud import texttospeech


class TextToSpeechClient:
    """Thin wrapper around Google Cloud TTS client for reuse across TTS files."""

    def __init__(self, credentials_path: str = None):
        """Initialize with optional path to JSON key file."""
        if credentials_path:
            self.client = texttospeech.TextToSpeechClient.from_service_account_json(
                credentials_path
            )
        else:
            self.client = texttospeech.TextToSpeechClient()

    def synthesize(
        self,
        input_data: texttospeech.SynthesisInput,
        voice: texttospeech.VoiceSelectionParams = None,
        audio_config: texttospeech.AudioConfig = None,
    ) -> texttospeech.SynthesizeSpeechResponse:
        """Delegate synthesis to the underlying Google TTS client."""
        if audio_config is None:
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
            )
        return self.client.synthesize_speech(
            input=input_data, voice=voice, audio_config=audio_config
        )
