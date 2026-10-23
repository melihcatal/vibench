from __future__ import annotations

from typing import Optional

from model_client import get_platform_client, DEFAULT_TTS_MODEL
from model_models import AudioResult


DEFAULT_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def generate_platform_brief_audio(
    text: str,
    model: str = DEFAULT_TTS_MODEL,
    voice: str = "alloy",
    response_format: str = "mp3",
    speed: float = 1.0,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> AudioResult:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    result = client.create_speech(
        text=text,
        model=model,
        voice=voice,
        response_format=response_format,
        speed=speed,
    )

    return AudioResult(
        audio_data=result["audio_data"],
        model_id=result["model"],
        format=result["format"],
        raw_response=result["raw_response"],
    )


def generate_briefing_with_voice(
    text: str,
    voice: str = "nova",
    model: str = DEFAULT_TTS_MODEL,
    response_format: str = "mp3",
    speed: float = 1.0,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> AudioResult:
    if voice not in DEFAULT_VOICES:
        raise ValueError(
            f"Voice '{voice}' not available. Choose from: {DEFAULT_VOICES}"
        )

    return generate_platform_brief_audio(
        text=text,
        model=model,
        voice=voice,
        response_format=response_format,
        speed=speed,
        api_key=api_key,
        organization=organization,
        project=project,
    )


def generate_multi_voice_briefing(
    segments: list[dict],
    model: str = DEFAULT_TTS_MODEL,
    response_format: str = "mp3",
    speed: float = 1.0,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> list[AudioResult]:
    results = []
    for segment in segments:
        text = segment["text"]
        voice = segment.get("voice", "alloy")

        if voice not in DEFAULT_VOICES:
            raise ValueError(
                f"Voice '{voice}' not available. Choose from: {DEFAULT_VOICES}"
            )

        result = generate_platform_brief_audio(
            text=text,
            model=model,
            voice=voice,
            response_format=response_format,
            speed=speed,
            api_key=api_key,
            organization=organization,
            project=project,
        )
        results.append(result)
    return results


def save_audio_to_file(
    audio_result: AudioResult,
    filepath: str,
) -> str:
    with open(filepath, "wb") as f:
        f.write(audio_result.audio_data)
    return filepath
