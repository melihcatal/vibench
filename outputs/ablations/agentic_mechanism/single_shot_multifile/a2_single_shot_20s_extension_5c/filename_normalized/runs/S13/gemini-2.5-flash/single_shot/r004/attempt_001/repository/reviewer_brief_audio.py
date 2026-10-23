import os
from elevenlabs.client import ElevenLabs
from elevenlabs.types import Voice, VoiceSettings

from safety_client import get_elevenlabs_client

def generate_reviewer_brief_audio(brief_text: str, voice_id: str = "21m00Tcm4obsnIqeld6m") -> bytes:
    eleven_client = get_elevenlabs_client()
    
    audio = eleven_client.generate(
        text=brief_text,
        voice=Voice(
            voice_id=voice_id,
            settings=VoiceSettings(stability=0.75, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
        ),
        model="eleven_multilingual_v2"
    )
    
    return audio