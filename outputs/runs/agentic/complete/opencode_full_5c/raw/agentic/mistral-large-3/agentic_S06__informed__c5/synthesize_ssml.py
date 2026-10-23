from typing import Optional, List
from speech_client import PollySpeechClient
from speech_models import Voice, normalize_voice_list


class SSMLSpeechSynthesizer:
    """Synthesizes SSML with voice and prosody controls using Amazon Polly."""

    def __init__(self):
        self.client = PollySpeechClient()

    def synthesize(self, ssml: str, voice_id: str) -> bytes:
        """Synthesize SSML to audio bytes."""
        return self.client.synthesize(ssml, voice_id, text_type="ssml")

    def list_voices(self, language_code: Optional[str] = None) -> List[Voice]:
        """List available voices for a target locale."""
        response = self.client.list_voices(language_code)
        return normalize_voice_list(response)
