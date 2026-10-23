import os
import base64
from typing import Optional
from translation_models import (
    AudioPreviewRequest,
    AudioPreviewResult,
    normalize_language_code,
)
from translation_client import (
    GoogleTextToSpeechClient,
    GOOGLE_TRANSLATE_API_KEY,
    GOOGLE_TTS_API_ENDPOINT,
    create_tts_client,
)


def generate_audio_preview(
    text: str,
    language_code: str,
    voice_name: Optional[str] = None,
    encoding: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    api_key: Optional[str] = None,
) -> AudioPreviewResult:
    client = create_tts_client(api_key=api_key)
    if voice_name is None:
        voice_name = client._get_default_voice(language_code)
    response = client.synthesize(
        text=text,
        language_code=language_code,
        voice_name=voice_name,
        encoding=encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    audio_content = base64.b64decode(response.get("audioContent", ""))
    duration_seconds = _estimate_duration(text, language_code, speaking_rate)
    return AudioPreviewResult(
        audio_content=audio_content,
        language_code=normalize_language_code(language_code),
        voice_name=voice_name,
        encoding=encoding,
        duration_seconds=duration_seconds,
    )


def generate_preview_for_translations(
    translated_texts: list,
    target_language: str,
    voice_name: Optional[str] = None,
    encoding: str = "MP3",
    api_key: Optional[str] = None,
) -> list:
    results = []
    for text in translated_texts:
        if text.strip():
            result = generate_audio_preview(
                text=text,
                language_code=target_language,
                voice_name=voice_name,
                encoding=encoding,
                api_key=api_key,
            )
            results.append(result)
    return results


def _estimate_duration(text: str, language_code: str, speaking_rate: float) -> float:
    word_count = len(text.split())
    lang = normalize_language_code(language_code).lower()
    wpm_map = {
        "en-us": 150,
        "en-gb": 145,
        "es-es": 160,
        "fr-fr": 155,
        "de-de": 140,
        "ja-jp": 300,
        "zh-cn": 250,
        "ko-kr": 220,
        "pt-br": 155,
        "it-it": 150,
        "ru-ru": 130,
        "ar-xa": 140,
        "hi-in": 160,
    }
    wpm = wpm_map.get(lang, 150)
    adjusted_wpm = wpm * speaking_rate
    if adjusted_wpm <= 0:
        adjusted_wpm = wpm
    return (word_count / adjusted_wpm) * 60


def save_audio_to_file(result: AudioPreviewResult, filepath: str) -> str:
    with open(filepath, "wb") as f:
        f.write(result.audio_content)
    return filepath


def get_voice_options_for_language(language_code: str) -> list:
    lang = normalize_language_code(language_code).lower()
    voice_map = {
        "en-us": [
            "en-US-Wavenet-A",
            "en-US-Wavenet-B",
            "en-US-Wavenet-C",
            "en-US-Wavenet-D",
        ],
        "en-gb": [
            "en-GB-Wavenet-A",
            "en-GB-Wavenet-B",
            "en-GB-Wavenet-C",
            "en-GB-Wavenet-D",
        ],
        "es-es": [
            "es-ES-Wavenet-A",
            "es-ES-Wavenet-B",
            "es-ES-Wavenet-C",
            "es-ES-Wavenet-D",
        ],
        "fr-fr": [
            "fr-FR-Wavenet-A",
            "fr-FR-Wavenet-B",
            "fr-FR-Wavenet-C",
            "fr-FR-Wavenet-D",
        ],
        "de-de": [
            "de-DE-Wavenet-A",
            "de-DE-Wavenet-B",
            "de-DE-Wavenet-C",
            "de-DE-Wavenet-D",
        ],
        "ja-jp": [
            "ja-JP-Wavenet-A",
            "ja-JP-Wavenet-B",
            "ja-JP-Wavenet-C",
            "ja-JP-Wavenet-D",
        ],
        "zh-cn": [
            "cmn-CN-Wavenet-A",
            "cmn-CN-Wavenet-B",
            "cmn-CN-Wavenet-C",
            "cmn-CN-Wavenet-D",
        ],
        "ko-kr": [
            "ko-KR-Wavenet-A",
            "ko-KR-Wavenet-B",
            "ko-KR-Wavenet-C",
            "ko-KR-Wavenet-D",
        ],
        "pt-br": [
            "pt-BR-Wavenet-A",
            "pt-BR-Wavenet-B",
            "pt-BR-Wavenet-C",
            "pt-BR-Wavenet-D",
        ],
        "it-it": [
            "it-IT-Wavenet-A",
            "it-IT-Wavenet-B",
            "it-IT-Wavenet-C",
            "it-IT-Wavenet-D",
        ],
        "ru-ru": [
            "ru-RU-Wavenet-A",
            "ru-RU-Wavenet-B",
            "ru-RU-Wavenet-C",
            "ru-RU-Wavenet-D",
        ],
        "ar-xa": ["ar-XA-Wavenet-A", "ar-XA-Wavenet-B", "ar-XA-Wavenet-C"],
        "hi-in": ["hi-IN-Wavenet-A", "hi-IN-Wavenet-B", "hi-IN-Wavenet-C"],
    }
    return voice_map.get(lang, ["en-US-Wavenet-D"])
