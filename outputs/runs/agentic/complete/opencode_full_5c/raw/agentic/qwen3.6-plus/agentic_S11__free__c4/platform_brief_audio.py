from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import PlatformClientConfig, create_openai_client
from model_models import (
    AudioResult,
    PlatformMessage,
    PlatformRequest,
    PlatformResponse,
    MessageRole,
    normalize_openai_response,
)

OPENAI_TTS_MODELS = ["tts-1", "tts-1-hd"]
OPENAI_TTS_VOICES = ["alloy", "echo", "fidget", "nova", "onyx", "shimmer"]
OPENAI_TTS_FORMATS = ["mp3", "opus", "aac", "flac", "wav", "pcm"]


def generate_platform_brief_audio(
    text: str,
    voice: str = "nova",
    model: str = "tts-1",
    response_format: str = "mp3",
    speed: float = 1.0,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> AudioResult:
    if voice not in OPENAI_TTS_VOICES:
        voice = "nova"
    if model not in OPENAI_TTS_MODELS:
        model = "tts-1"
    if response_format not in OPENAI_TTS_FORMATS:
        response_format = "mp3"

    openai_client = client or create_openai_client(config)

    response = openai_client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format=response_format,
        speed=speed,
    )

    audio_bytes = response.content

    return AudioResult(
        audio_data=audio_bytes,
        format=response_format,
        model=model,
        raw=response,
    )


def generate_briefing_from_platform_output(
    platform_response: PlatformResponse,
    voice: str = "nova",
    model: str = "tts-1-hd",
    response_format: str = "mp3",
    summarize: bool = True,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> AudioResult:
    text_to_speak = platform_response.content

    if summarize and len(text_to_speak) > 500:
        summary_request = PlatformRequest(
            messages=[
                PlatformMessage(
                    role=MessageRole.SYSTEM,
                    content="Summarize the following text into a brief spoken-style summary of 2-3 sentences.",
                ),
                PlatformMessage(role=MessageRole.USER, content=text_to_speak),
            ],
            model="gpt-4o",
            temperature=0.3,
            max_tokens=200,
        )

        openai_client = client or create_openai_client(config)
        payload = summary_request.to_openai_payload()
        raw_summary = openai_client.chat.completions.create(**payload)
        summary = normalize_openai_response(raw_summary)
        text_to_speak = summary.content

    return generate_platform_brief_audio(
        text=text_to_speak,
        voice=voice,
        model=model,
        response_format=response_format,
        client=openai_client if summarize else None,
        config=config,
    )


def save_audio_result(result: AudioResult, filepath: str) -> str:
    with open(filepath, "wb") as f:
        f.write(result.audio_data)
    return filepath


if __name__ == "__main__":
    audio = generate_platform_brief_audio(
        text="Welcome to today's briefing. The weather is sunny and warm.",
        voice="nova",
        model="tts-1",
    )
    print(f"Audio generated: {len(audio.audio_data)} bytes, format: {audio.format}")
