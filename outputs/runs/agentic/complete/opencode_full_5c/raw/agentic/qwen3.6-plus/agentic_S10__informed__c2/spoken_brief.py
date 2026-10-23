import os
from typing import Optional

from elevenlabs import ElevenLabs, VoiceSettings

from model_models import SpeechResult


def _get_elevenlabs_client() -> ElevenLabs:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is not set")
    return ElevenLabs(api_key=api_key)


def generate_spoken_brief(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    model: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity: float = 0.75,
    style: float = 0.0,
) -> SpeechResult:
    client = _get_elevenlabs_client()
    audio_generator = client.generate(
        text=text,
        voice=voice_id,
        model=model,
        voice_settings=VoiceSettings(
            stability=stability,
            similarity_boost=similarity,
            style=style,
        ),
    )
    audio_bytes = b"".join(audio_generator)
    return SpeechResult(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
    )


def generate_spoken_brief_to_file(
    text: str,
    output_path: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    model: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity: float = 0.75,
) -> str:
    result = generate_spoken_brief(
        text,
        voice_id=voice_id,
        model=model,
        stability=stability,
        similarity=similarity,
    )
    with open(output_path, "wb") as f:
        f.write(result.audio_bytes)
    return output_path


def list_available_voices() -> list[dict]:
    client = _get_elevenlabs_client()
    voices = client.voices.get_all()
    result = []
    for voice in voices.voices:
        result.append(
            {
                "voice_id": voice.voice_id,
                "name": voice.name,
                "category": voice.category,
                "labels": voice.labels,
            }
        )
    return result


def generate_brief_from_model_output(
    model_output: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    model: str = "eleven_multilingual_v2",
    max_chars: int = 5000,
) -> SpeechResult:
    truncated = model_output[:max_chars]
    if len(model_output) > max_chars:
        truncated += "..."
    return generate_spoken_brief(
        truncated,
        voice_id=voice_id,
        model=model,
    )
