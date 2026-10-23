import os
from elevenlabs import generate, set_api_key


class AudioBriefGenerator:
    """Generate a spoken brief from retrieved search results using ElevenLabs."""

    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable not set")
        set_api_key(self.api_key)

    def generate_brief(self, text: str, voice: str = "Rachel") -> bytes:
        audio = generate(text=text, voice=voice, model="eleven_multilingual_v2")
        return audio


def generate_audio_brief(text: str) -> bytes:
    return AudioBriefGenerator().generate_brief(text)