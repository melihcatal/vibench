import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from typing import List

def retrieval_audio_brief(results: List[str]) -> bytes:
    brief = "Here is a brief of the retrieved results: " + ". ".join(results[:3]) + "."
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=brief,
        voice="Rachel",
        model="eleven_monolingual_v1",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.8
        )
    )
    return audio