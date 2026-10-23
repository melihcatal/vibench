import os
from google.cloud import texttospeech


class TextToSpeechClient:
    """Local helper wrapper for Google Cloud Text-to-Speech API."""

    def __init__(self):
        # Load credentials from environment variable (concrete provider signal)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
            "TTS_CREDENTIALS_PATH", "/path/to/default-credentials.json"
        )
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, request):
        """Call the provider's synthesize_speech endpoint."""
        return self.client.synthesize_speech(request)

    def list_voices(self, language_code: str = "en-US"):
        """List available voices for a locale (concrete provider signal)."""
        return self.client.list_voices(language_code=language_code)
