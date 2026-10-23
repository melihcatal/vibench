import os
from typing import Optional

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs


class SpokenBriefClient:
    """Client for ElevenLabs Text to Speech API."""

    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable not set")
        self.client = ElevenLabs(api_key=self.api_key)

    def generate_spoken_brief(self, text: str, voice_id: Optional[str] = None) -> bytes:
        """Generate spoken brief from text using ElevenLabs API."""
        audio = self.client.generate(
            text=text,
            voice=voice_id or "Rachel",
            model="eleven_multilingual_v2",
            voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75),
        )
        return b"".join(audio)


def generate_spoken_brief(text: str, voice_id: Optional[str] = None) -> bytes:
    """Generate a spoken brief from model output using ElevenLabs API."""
    client = SpokenBriefClient()
    return client.generate_spoken_brief(text, voice_id)
