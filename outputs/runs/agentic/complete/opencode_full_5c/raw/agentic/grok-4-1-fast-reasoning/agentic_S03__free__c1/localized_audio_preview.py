from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import os


def localized_audio_preview(text: str, lang: str = "en") -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.75),
    )
    return audio
