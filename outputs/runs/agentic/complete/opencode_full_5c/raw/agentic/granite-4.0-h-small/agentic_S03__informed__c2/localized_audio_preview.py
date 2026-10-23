# [LATER-STEP] localized_audio_preview.py

# Generate spoken previews of translated copy using ElevenLabs Text-to-Speech API.
import os
import json
from elevenlabs import ElevenLabs

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise RuntimeError("Set ELEVENLABS_API_KEY environment variable")


def generate_audio_previews(
    translated_texts: list[str], voice_id: str = "1L8mV74zr9Lq8VMX8DRA"
) -> list[bytes]:
    """Generate audio (as bytes) for each translated text using ElevenLabs TTS.","""
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audios = []
    for txt in translated_texts:
        resp = client.get_audio(text=txt, voice_id=voice_id, model="11/v1")
        audios.append(resp["audio_content"])  # audio_content is binary data
    return audios
