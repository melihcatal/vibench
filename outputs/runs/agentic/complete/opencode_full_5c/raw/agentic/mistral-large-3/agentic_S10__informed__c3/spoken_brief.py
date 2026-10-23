import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from typing import Optional


class SpokenBriefGenerator:
    def __init__(self, voice_id: Optional[str] = None):
        self.voice_id = voice_id or "pNInz6obpgDQGcFmaJgB"
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def generate(self, text: str, output_file: str = "spoken_brief.mp3") -> str:
        audio = self.client.generate(
            text=text,
            voice=self.client.voices.get(self.voice_id),
            model="eleven_multilingual_v2",
            voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.5),
        )
        self.client.generate(
            text=text,
            voice=self.client.voices.get(self.voice_id),
            model="eleven_multilingual_v2",
            output=output_file,
        )
        return output_file
