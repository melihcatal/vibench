import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from typing import Union


def platform_brief_audio(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_monolingual_v1",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.5,
            style=0.5,
            use_speaker_boost=True,
        ),
        output_format="mp3_22050_32",
    )
    return audio
