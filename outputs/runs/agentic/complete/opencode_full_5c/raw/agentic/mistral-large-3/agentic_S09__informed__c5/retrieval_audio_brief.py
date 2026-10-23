from typing import List, Dict, Any
import os
from elevenlabs import generate, set_api_key


class AudioBriefGenerator:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        set_api_key(self.api_key)

    def generate_spoken_brief(self, text: str, voice: str = "Rachel") -> bytes:
        """
        Generates a spoken brief from retrieved search results using ElevenLabs TTS.
        """
        audio = generate(text=text, voice=voice, model="eleven_multilingual_v2")
        return audio
