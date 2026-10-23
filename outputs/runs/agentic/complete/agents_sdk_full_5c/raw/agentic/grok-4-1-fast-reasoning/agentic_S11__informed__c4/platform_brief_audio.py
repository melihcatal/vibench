import os
from elevenlabs.client import ElevenLabs
from elevenlabs.commons import AudioOutputFormat
from typing import Union

def generate_platform_brief_audio(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # default voice
    model_id: str = "eleven_turbo_v2_5"
) -> bytes:
    """
    Generate spoken briefings from platform outputs using ElevenLabs TTS.
    """
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=AudioOutputFormat.MP3_44100_128,
        optimize_streaming_latency=0
    )
    return audio
