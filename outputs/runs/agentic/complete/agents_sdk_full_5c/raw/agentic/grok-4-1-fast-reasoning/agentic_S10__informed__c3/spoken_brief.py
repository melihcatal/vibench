import os
from elevenlabs.client import ElevenLabs
from elevenlabs.commons import VoiceSettings

def generate_spoken_brief(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(api_key=api_key)
    
    audio = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_monolingual_v1",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True,
        )
    )
    return audio