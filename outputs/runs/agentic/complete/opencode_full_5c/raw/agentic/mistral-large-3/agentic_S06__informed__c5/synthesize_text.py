from typing import Optional, List
from speech_client import PollySpeechClient
from speech_models import Voice, normalize_voice_list


class TextToSpeechSynthesizer:
    """Synthesizes plain text to an audio byte stream using Amazon Polly."""

    def __init__(self):
        self.client = PollySpeechClient()

    def synthesize(self, text: str, voice_id: str) -> bytes:
        """Synthesize plain text to audio bytes."""
        return self.client.synthesize(text, voice_id, text_type="text")

    def list_voices(self, language_code: Optional[str] = None) -> List[Voice]:
        """List available voices for a target locale."""
        response = self.client.list_voices(language_code)
        return normalize_voice_list(response)
