import os
import base64
import tempfile
from typing import Optional
import openai
from translation_models import (
    AudioPreviewRequest,
    AudioPreviewResponse,
    normalize_language_code,
)

OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"
TTS_MODEL = "tts-1"

LANGUAGE_VOICE_MAP = {
    "EN": "alloy",
    "EN-US": "alloy",
    "EN-GB": "echo",
    "ES": "nova",
    "FR": "shimmer",
    "DE": "onyx",
    "IT": "fable",
    "PT": "nova",
    "PT-BR": "nova",
    "JA": "echo",
    "ZH": "shimmer",
    "KO": "onyx",
    "RU": "fable",
    "AR": "echo",
}


def get_openai_client() -> openai.OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return openai.OpenAI(api_key=api_key)


def resolve_voice(language: str, requested_voice: Optional[str] = None) -> str:
    if requested_voice:
        return requested_voice
    lang_upper = normalize_language_code(language)
    return LANGUAGE_VOICE_MAP.get(lang_upper, "alloy")


def generate_audio_preview(request: AudioPreviewRequest) -> AudioPreviewResponse:
    client = get_openai_client()
    voice = resolve_voice(request.language, request.voice_id)
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=voice,
        input=request.text,
        speed=request.speed,
        response_format="mp3",
    )
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        response.stream_to_file(tmp.name)
        audio_url = f"file://{tmp.name}"
    estimated_duration = len(request.text) / 15.0 * (1.0 / request.speed)
    return AudioPreviewResponse(
        audio_url=audio_url,
        language=request.language,
        duration_seconds=round(estimated_duration, 2),
        voice_id=voice,
        model=TTS_MODEL,
    )


def generate_audio_preview_base64(request: AudioPreviewRequest) -> AudioPreviewResponse:
    client = get_openai_client()
    voice = resolve_voice(request.language, request.voice_id)
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=voice,
        input=request.text,
        speed=request.speed,
        response_format="mp3",
    )
    audio_bytes = response.content
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    audio_url = f"data:audio/mp3;base64,{audio_base64}"
    estimated_duration = len(request.text) / 15.0 * (1.0 / request.speed)
    return AudioPreviewResponse(
        audio_url=audio_url,
        language=request.language,
        duration_seconds=round(estimated_duration, 2),
        voice_id=voice,
        model=TTS_MODEL,
    )
