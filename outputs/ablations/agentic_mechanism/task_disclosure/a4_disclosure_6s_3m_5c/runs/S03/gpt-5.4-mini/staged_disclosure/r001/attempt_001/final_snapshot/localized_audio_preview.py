import base64
import json
import os
from dataclasses import dataclass
from typing import Optional
from urllib import error, request


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"


@dataclass
class AudioPreviewResult:
    audio_bytes: bytes
    content_type: str


def _build_payload(text: str, language: str, voice: str, model: str) -> bytes:
    prompt = f"Read the following translated copy naturally in {language}: {text}"
    payload = {
        "model": model,
        "input": prompt,
        "voice": voice,
        "response_format": "mp3",
    }
    return json.dumps(payload).encode("utf-8")


def generate_spoken_preview(translated_copy: str, language: str, voice: str = "alloy", model: str = OPENAI_TTS_MODEL, api_key: Optional[str] = None) -> AudioPreviewResult:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI TTS generation")

    req = request.Request(
        OPENAI_TTS_ENDPOINT,
        data=_build_payload(translated_copy, language, voice, model),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            content_type = resp.headers.get_content_type()
            return AudioPreviewResult(audio_bytes=resp.read(), content_type=content_type)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI TTS request failed: {exc.code} {detail}") from exc


def save_preview(result: AudioPreviewResult, output_path: str) -> str:
    with open(output_path, "wb") as f:
        f.write(result.audio_bytes)
    return output_path


def preview_to_base64(result: AudioPreviewResult) -> str:
    return base64.b64encode(result.audio_bytes).decode("ascii")


def make_localized_audio_preview(translated_copy: str, language: str, output_path: Optional[str] = None, voice: str = "alloy", api_key: Optional[str] = None) -> str:
    result = generate_spoken_preview(translated_copy, language, voice=voice, api_key=api_key)
    if output_path:
        return save_preview(result, output_path)
    return preview_to_base64(result)
