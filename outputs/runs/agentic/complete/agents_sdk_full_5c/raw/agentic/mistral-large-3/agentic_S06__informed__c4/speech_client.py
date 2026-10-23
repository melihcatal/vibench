import os
from elevenlabs import ElevenLabs
from typing import Optional


class SpeechClient:
    """
    Client helper for ElevenLabs Text-to-Speech.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable not set")
        self.client = ElevenLabs(api_key=self.api_key)

    def get_client(self) -> ElevenLabs:
        return self.client


def get_speech_client() -> SpeechClient:
    """
    Initialize and return a SpeechClient instance.
    """
    return SpeechClient()