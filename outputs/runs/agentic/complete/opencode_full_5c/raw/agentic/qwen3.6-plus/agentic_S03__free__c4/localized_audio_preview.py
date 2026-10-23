import base64
from typing import Optional

from translation_client import generate_audio_preview
from translation_models import AudioPreviewRequest, AudioPreviewResult


GOOGLE_TTS_API_BASE = "https://texttospeech.googleapis.com"

VOICE_MAP = {
    "en": "en-US-Wavenet-D",
    "es": "es-ES-Standard-A",
    "fr": "fr-FR-Standard-A",
    "de": "de-DE-Standard-A",
    "it": "it-IT-Standard-A",
    "pt": "pt-PT-Standard-A",
    "pt-BR": "pt-BR-Wavenet-A",
    "ja": "ja-JP-Standard-A",
    "ko": "ko-KR-Standard-A",
    "zh-CN": "cmn-CN-Wavenet-A",
    "zh-TW": "cmn-TW-Standard-A",
    "ru": "ru-RU-Standard-A",
    "ar": "ar-XA-Standard-A",
    "hi": "hi-IN-Standard-A",
    "nl": "nl-NL-Standard-A",
    "pl": "pl-PL-Standard-A",
    "tr": "tr-TR-Standard-A",
    "sv": "sv-SE-Standard-A",
    "da": "da-DK-Standard-A",
    "fi": "fi-FI-Standard-A",
    "no": "nb-NO-Standard-A",
}


def generate_localized_audio(
    text: str,
    language_code: str,
    voice_name: Optional[str] = None,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    api_key: Optional[str] = None,
) -> AudioPreviewResult:
    selected_voice = voice_name or VOICE_MAP.get(language_code)

    request = AudioPreviewRequest(
        text=text,
        language_code=language_code,
        voice_name=selected_voice,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    audio_bytes = generate_audio_preview(
        text=request.text,
        language_code=request.language_code,
        voice_name=request.voice_name,
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
        api_key=api_key,
    )

    duration_seconds = _estimate_audio_duration(text, request.speaking_rate)

    return AudioPreviewResult(
        audio_content=audio_bytes,
        audio_format="mp3",
        duration_seconds=duration_seconds,
    )


def generate_localized_audio_with_config(
    config: AudioPreviewRequest,
    api_key: Optional[str] = None,
) -> AudioPreviewResult:
    return generate_localized_audio(
        text=config.text,
        language_code=config.language_code,
        voice_name=config.voice_name,
        speaking_rate=config.speaking_rate,
        pitch=config.pitch,
        api_key=api_key,
    )


def generate_batch_audio_previews(
    texts: list[str],
    language_code: str,
    voice_name: Optional[str] = None,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    api_key: Optional[str] = None,
) -> list[AudioPreviewResult]:
    results: list[AudioPreviewResult] = []
    for text in texts:
        result = generate_localized_audio(
            text=text,
            language_code=language_code,
            voice_name=voice_name,
            speaking_rate=speaking_rate,
            pitch=pitch,
            api_key=api_key,
        )
        results.append(result)
    return results


def _estimate_audio_duration(text: str, speaking_rate: float) -> float:
    word_count = len(text.split())
    words_per_minute = 150 * speaking_rate
    if words_per_minute <= 0:
        words_per_minute = 150
    duration_seconds = (word_count / words_per_minute) * 60
    return round(duration_seconds, 2)


def encode_audio_to_base64(audio_result: AudioPreviewResult) -> str:
    return base64.b64encode(audio_result.audio_content).decode("utf-8")
