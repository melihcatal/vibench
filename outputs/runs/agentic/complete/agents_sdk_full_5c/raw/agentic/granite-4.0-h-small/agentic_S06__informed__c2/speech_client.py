import os
from typing import Optional, Dict, Any

# Provider‑specific imports for Google Cloud Text‑to‑Speech
from google.cloud import texttospeech

# Helper to locate credentials
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


class SpeechClient:
    """Thin wrapper around Google Cloud TTS client library.

    Identifies the provider with the import `google.cloud.texttospeech`.
    """
    def __init__(self):
        # Configure client; credentials are auto‑discovered from env var
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, input_text: str, voice_name: str, voice_locale: Optional[str] = None) -> Any:
        """Call the provider’s `synthesize_speech` with plain text.

        Returns an object containing `audio_content` (bytes) and other metadata.
        """
        synthesis_input = texttospeech.SynthesisInput(text=input_text)
        voice = texttospeech.VoiceSelectionParams(language_code=voice_locale or "en-US",
                                                   name=voice_name)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response  # Has .audio_content & .metadata attributes

    def list_voices(self, locale: str = None, search_term: Optional[str] = None) -> Any:
        """List voices; optional locale filter and optional search term.
        Returns the provider's Voice data structure.
        """
        voice_filter = f"language_code = '{locale}'" if locale else None
        return self.client.list_voices(language_code=locale, name=search_term)

    def resolve_path(self, target_path: str) -> tuple[Optional[str], str]:
        """Parse a target path to decide whether it is a cloud storage URI.
        For Google Cloud Storage the schema is `gs://bucket/path`.
        Returns (bucket_name, blob_name), None for bucket_name if not a storage URI.
        """
        if target_path.startswith("gs://"):
            parts = target_path[5:].split('/', 1)
            bucket_name = parts[0]
            blob_name = parts[1] if len(parts) > 1 else ""
            return bucket_name, blob_name
        return None, target_path

    @classmethod
    def get_client(cls) -> 'SpeechClient':
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance
