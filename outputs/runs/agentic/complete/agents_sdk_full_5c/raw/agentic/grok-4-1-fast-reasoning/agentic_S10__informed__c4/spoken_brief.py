import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

def generate_spoken_brief(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
        ),
        output_format="mp3_22050_32"
    )
    return audio
