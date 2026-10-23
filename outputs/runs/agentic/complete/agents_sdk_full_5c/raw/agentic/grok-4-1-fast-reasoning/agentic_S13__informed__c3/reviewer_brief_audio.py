import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from typing import Iterator

def generate_reviewer_brief_audio(brief_text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY must be set")
    client = ElevenLabs(api_key=api_key)
    voice = VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
        style=0.0,
        use_speaker_boost=True,
    )
    audio_stream: Iterator[bytes] = client.text_to_speech.convert_text_to_audio(
        text=brief_text,
        voice_id=voice_id,
        voice_settings=voice,
        output_format="mp3_44100_128"
    )
    audio_bytes = b"".join(audio_stream)
    return audio_bytes
