import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

def generate_localized_audio(text: str, voice_id: str = "pNInz6obpgDQGcFmaJgB") -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
    )
    return audio