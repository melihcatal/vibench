import os
from typing import Optional

from elevenlabs import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
DEFAULT_VOICE_ID = "pNInz6obpgDQGcFmaJgB"


def _build_brief_text(moderation_summary: dict) -> str:
    parts = [
        f"Moderation review brief.",
        f"Total items reviewed: {moderation_summary.get('total_reviewed', 0)}.",
        f"Flagged items: {moderation_summary.get('flagged_count', 0)}.",
        f"Blocked items: {moderation_summary.get('blocked_count', 0)}.",
    ]
    summary = moderation_summary.get("summary", "")
    if summary:
        parts.append(f"Summary: {summary}")
    return " ".join(parts)


def generate_reviewer_audio(
    moderation_summary: dict,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = "eleven_multilingual_v2",
) -> dict:
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    brief_text = _build_brief_text(moderation_summary)

    audio_generator = client.text_to_speech.convert(
        text=brief_text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )

    audio_bytes = b""
    for chunk in audio_generator:
        audio_bytes += chunk

    return {
        "audio_data": audio_bytes,
        "audio_length_bytes": len(audio_bytes),
        "brief_text": brief_text,
        "voice_id": voice_id,
        "model_id": model_id,
        "provider": "elevenlabs",
    }


def generate_audio_from_text(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = "eleven_multilingual_v2",
) -> dict:
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio_generator = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
    )

    audio_bytes = b""
    for chunk in audio_generator:
        audio_bytes += chunk

    return {
        "audio_data": audio_bytes,
        "audio_length_bytes": len(audio_bytes),
        "input_text": text,
        "voice_id": voice_id,
        "model_id": model_id,
        "provider": "elevenlabs",
    }


def list_available_voices() -> list[dict]:
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    voices = client.voices.get_all()
    result = []
    for voice in voices.voices:
        result.append(
            {
                "voice_id": voice.voice_id,
                "name": voice.name,
                "category": voice.category or "unknown",
                "provider": "elevenlabs",
            }
        )
    return result
