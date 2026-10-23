# [HELPER] speech_client.py

import os
from typing import Optional
from google.cloud import texttospeech

class TextToSpeechClient:
    """Facade for Google Cloud Text-to-Speech with sensible defaults and credential handling.

    Attributes:
        client: Underlying google.cloud.texttospeech.TextToSpeechClient instance.
        default_voice: BCP-47 language tag for the default voice (e.g., 'en-US').
    """

    def __init__(self, credentials_path: Optional[str] = None):
        creds = None
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        else:
            # Load default creds from env or service account attached to runtime.
            creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.client = texttospeech.TextToSpeechClient()
        self.default_voice = "en-US"  # change to your preferred default if needed
        # Verify credentials loaded; raise helpful message if missing.
        if not creds:
            raise RuntimeError(
                "Google Cloud credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS or pass a path."
            )

    def synthesize(self, text: str, voice: Optional[str] = None, **kwargs):
        """Convenient wrapper that dispatches to the appropriate synthesis method (plain text or SSML)."""
        if kwargs.get("ssml"):
            return synthesize_ssml(self, text, voice=voice, **kwargs)
        else:
            return synthesize_text(self, text, voice=voice, **kwargs)
