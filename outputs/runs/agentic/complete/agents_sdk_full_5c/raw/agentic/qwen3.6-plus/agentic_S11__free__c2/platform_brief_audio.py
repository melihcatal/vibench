"""Generate spoken briefings from platform outputs using OpenAI text-to-speech."""

import os

from openai import OpenAI

from model_client import get_openai_client
from model_models import PlatformResponse


_OPENAI_TTS_MODEL = "tts-1"
_OPENAI_TTS_VOICE = "alloy"
_OPENAI_TTS_FORMAT = "mp3"


def platform_brief_audio(
    response: PlatformResponse,
    *,
    tts_model: str = _OPENAI_TTS_MODEL,
    voice: str = _OPENAI_TTS_VOICE,
    output_path: str | None = None,
) -> bytes:
    """Generate a spoken audio briefing from the text in a PlatformResponse.

    Uses the OpenAI Text-to-Speech API at api.openai.com with the
    tts-1 model and the alloy voice to convert the model output into
    an MP3 audio buffer suitable for playback or storage.
    """
    client = get_openai_client()

    speech_bytes: bytes = b""
    with client.audio.speech.with_streaming_response.create(
        model=tts_model,
        voice=voice,
        response_format=_OPENAI_TTS_FORMAT,
        input=response.text,
    ) as audio_response:
        speech_bytes = audio_response.content

    if output_path:
        _save_audio(speech_bytes, output_path)

    return speech_bytes


def generate_brief_audio_from_text(
    text: str,
    *,
    tts_model: str = _OPENAI_TTS_MODEL,
    voice: str = _OPENAI_TTS_VOICE,
    output_path: str | None = None,
) -> bytes:
    """Generate spoken audio from raw text using the OpenAI TTS API."""
    client = get_openai_client()

    speech_bytes: bytes = b""
    with client.audio.speech.with_streaming_response.create(
        model=tts_model,
        voice=voice,
        response_format=_OPENAI_TTS_FORMAT,
        input=text,
    ) as audio_response:
        speech_bytes = audio_response.content

    if output_path:
        _save_audio(speech_bytes, output_path)

    return speech_bytes


def _save_audio(data: bytes, path: str) -> None:
    """Write audio bytes to a file."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    resp = PlatformResponse(
        text="Welcome to your daily briefing. All systems are operational.",
        model="gpt-4o",
    )
    audio_data = platform_brief_audio(resp, output_path="brief.mp3")
    print(f"Generated {len(audio_data)} bytes of audio.")
