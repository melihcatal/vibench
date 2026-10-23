from typing import Dict, Any, Optional, BinaryIO
import os
from elevenlabs import generate, save, voices
from elevenlabs.api import Voice, VoiceSettings


def generate_briefing_audio_with_elevenlabs(
    text: str,
    voice_id: Optional[str] = None,
    api_key: Optional[str] = None,
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generates spoken briefings from platform model outputs using ElevenLabs TTS.
    Returns audio data and metadata, optionally saving to a file.
    """
    if api_key is None:
        api_key = os.getenv("ELEVENLABS_API_KEY")
    if api_key is None:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")

    if voice_id is None:
        available_voices = voices(api_key=api_key)
        voice_id = available_voices[0].voice_id

    audio = generate(text=text, voice=voice_id, api_key=api_key)

    result = {
        "audio_data": audio,
        "voice_id": voice_id,
        "text": text,
        "sample_rate": 44100,
        "bits_per_sample": 16,
        "channels": 1,
    }

    if output_path:
        save(audio, filename=output_path)
        result["output_path"] = output_path

    return result
