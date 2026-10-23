import os
import base64
import tempfile
from typing import List, Optional
from openai import OpenAI
from translation_models import AudioPreviewResult, normalize_language_code
from translation_client import get_openai_client

OPENAI_TTS_MODEL = "tts-1"
OPENAI_TTS_HD_MODEL = "tts-1-hd"
OPENAI_TTS_API_BASE = "https://api.openai.com/v1"

VOICE_MAP = {
    "en": "nova",
    "es": "alloy",
    "fr": "shimmer",
    "de": "onyx",
    "ja": "nova",
    "zh": "nova",
    "ko": "nova",
    "pt": "alloy",
    "ru": "onyx",
    "it": "shimmer",
    "ar": "onyx",
    "hi": "nova",
}

DEFAULT_VOICE = "nova"
DEFAULT_TTS_FORMAT = "mp3"


def get_voice_for_language(language_code: str) -> str:
    lang = normalize_language_code(language_code)
    return VOICE_MAP.get(lang, DEFAULT_VOICE)


def generate_audio_preview(
    text: str,
    language: str = "en",
    voice: Optional[str] = None,
    use_hd_model: bool = False,
    speed: float = 1.0,
    output_format: str = DEFAULT_TTS_FORMAT,
) -> AudioPreviewResult:
    client = get_openai_client()
    lang = normalize_language_code(language)
    selected_voice = voice if voice else get_voice_for_language(lang)
    tts_model = OPENAI_TTS_HD_MODEL if use_hd_model else OPENAI_TTS_MODEL

    response = client.audio.speech.create(
        model=tts_model,
        voice=selected_voice,
        input=text,
        response_format=output_format,
        speed=speed,
    )

    audio_bytes = response.content
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
    data_url = f"data:audio/{output_format};base64,{audio_b64}"

    estimated_duration = len(text.split()) * 0.4 / speed

    return AudioPreviewResult(
        audio_url=data_url,
        duration_seconds=estimated_duration,
        format=output_format,
        text_preview=text[:100] + ("..." if len(text) > 100 else ""),
    )


def generate_batch_audio_previews(
    texts: List[str],
    language: str = "en",
    voice: Optional[str] = None,
    use_hd_model: bool = False,
    speed: float = 1.0,
    output_format: str = DEFAULT_TTS_FORMAT,
) -> List[AudioPreviewResult]:
    results = []
    for text in texts:
        result = generate_audio_preview(
            text=text,
            language=language,
            voice=voice,
            use_hd_model=use_hd_model,
            speed=speed,
            output_format=output_format,
        )
        results.append(result)
    return results
