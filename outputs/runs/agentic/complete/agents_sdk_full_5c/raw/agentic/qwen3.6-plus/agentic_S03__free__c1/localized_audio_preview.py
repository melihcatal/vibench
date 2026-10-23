"""Generate spoken previews of translated copy using Google Cloud Text-to-Speech API."""

import os
import base64
import json
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from google.cloud import texttospeech
from google.cloud.texttospeech import enums, types
from translation_client import load_translation_config
from translation_models import TranslationResponse


GOOGLE_TTS_VOICES = {
    "en": ("en-US", "en-US-Wavenet-D"),
    "en-US": ("en-US", "en-US-Wavenet-D"),
    "en-GB": ("en-GB", "en-GB-Wavenet-A"),
    "es": ("es-ES", "es-ES-Wavenet-B"),
    "es-MX": ("es-MX", "es-MX-Wavenet-A"),
    "fr": ("fr-FR", "fr-FR-Wavenet-A"),
    "fr-CA": ("fr-CA", "fr-CA-Wavenet-A"),
    "de": ("de-DE", "de-DE-Wavenet-A"),
    "it": ("it-IT", "it-IT-Wavenet-A"),
    "pt": ("pt-PT", "pt-PT-Wavenet-A"),
    "pt-BR": ("pt-BR", "pt-BR-Wavenet-A"),
    "ja": ("ja-JP", "ja-JP-Wavenet-A"),
    "ko": ("ko-KR", "ko-KR-Wavenet-A"),
    "zh": ("cmn-CN", "cmn-CN-Wavenet-A"),
    "zh-CN": ("cmn-CN", "cmn-CN-Wavenet-A"),
    "zh-TW": ("cmn-TW", "cmn-TW-Wavenet-A"),
    "ru": ("ru-RU", "ru-RU-Wavenet-A"),
    "ar": ("ar-XA", "ar-XA-Wavenet-A"),
    "hi": ("hi-IN", "hi-IN-Wavenet-A"),
    "nl": ("nl-NL", "nl-NL-Wavenet-A"),
    "pl": ("pl-PL", "pl-PL-Wavenet-A"),
    "tr": ("tr-TR", "tr-TR-Wavenet-A"),
    "sv": ("sv-SE", "sv-SE-Wavenet-A"),
}


@dataclass
class AudioPreviewResult:
    """Result of audio preview generation."""
    text: str
    language: str
    voice_name: str
    audio_content_base64: str
    audio_format: str
    duration_estimate_ms: int
    character_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "language": self.language,
            "voice_name": self.voice_name,
            "audio_content_base64": self.audio_content_base64[:100] + "...",
            "audio_format": self.audio_format,
            "duration_estimate_ms": self.duration_estimate_ms,
            "character_count": self.character_count,
        }


def get_voice_for_language(language: str) -> tuple:
    """Get the appropriate Google Cloud TTS voice for a language.

    Args:
        language: Language code (e.g., 'en', 'es', 'fr').

    Returns:
        Tuple of (language_code, voice_name).
    """
    if language in GOOGLE_TTS_VOICES:
        return GOOGLE_TTS_VOICES[language]

    lang_prefix = language.split("-")[0].lower()
    for key, value in GOOGLE_TTS_VOICES.items():
        if key.startswith(lang_prefix) or key == lang_prefix:
            return value

    return ("en-US", "en-US-Wavenet-D")


def estimate_audio_duration_ms(text: str, language: str) -> int:
    """Estimate audio duration in milliseconds based on text length and language.

    Args:
        text: Text to be spoken.
        language: Language code.

    Returns:
        Estimated duration in milliseconds.
    """
    word_count = len(text.split())

    wpm_estimates = {
        "en": 150,
        "es": 140,
        "fr": 145,
        "de": 130,
        "it": 140,
        "pt": 145,
        "ja": 120,
        "ko": 130,
        "zh": 120,
        "ru": 130,
        "ar": 125,
    }

    lang_prefix = language.split("-")[0].lower()
    wpm = wpm_estimates.get(lang_prefix, 150)

    duration_minutes = word_count / wpm
    duration_ms = int(duration_minutes * 60 * 1000)

    return max(500, duration_ms)


def generate_audio_preview(
    text: str,
    language: str,
    audio_format: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
) -> AudioPreviewResult:
    """Generate a spoken audio preview of translated text using Google Cloud TTS.

    Args:
        text: Text to synthesize.
        language: Language code for voice selection.
        audio_format: Output audio format (MP3, LINEAR16, OGG_OPUS).
        speaking_rate: Speed of speech (0.25 to 4.0).
        pitch: Pitch adjustment (-20.0 to 20.0).

    Returns:
        AudioPreviewResult with base64-encoded audio and metadata.
    """
    config = load_translation_config()
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

    client = texttospeech.TextToSpeechClient()

    lang_code, voice_name = get_voice_for_language(language)

    synthesis_input = types.SynthesisInput(text=text)

    voice = types.VoiceSelectionParams(
        language_code=lang_code,
        name=voice_name,
    )

    format_map = {
        "MP3": enums.AudioEncoding.MP3,
        "LINEAR16": enums.AudioEncoding.LINEAR16,
        "OGG_OPUS": enums.AudioEncoding.OGG_OPUS,
        "MULAW": enums.AudioEncoding.MULAW,
    }

    audio_config = types.AudioConfig(
        audio_encoding=format_map.get(audio_format, enums.AudioEncoding.MP3),
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    audio_content = response.audio_content
    audio_base64 = base64.b64encode(audio_content).decode("utf-8")

    duration_ms = estimate_audio_duration_ms(text, language)

    return AudioPreviewResult(
        text=text,
        language=language,
        voice_name=voice_name,
        audio_content_base64=audio_base64,
        audio_format=audio_format,
        duration_estimate_ms=duration_ms,
        character_count=len(text),
    )


def generate_batch_audio_previews(
    translations: List[Dict[str, str]],
    target_lang: str,
    audio_format: str = "MP3",
) -> List[AudioPreviewResult]:
    """Generate audio previews for multiple translated texts.

    Args:
        translations: List of dicts with 'text' or 'translated' keys.
        target_lang: Target language for voice selection.
        audio_format: Output audio format.

    Returns:
        List of AudioPreviewResult objects.
    """
    results = []

    for trans in translations:
        text = trans.get("text", trans.get("translated", trans.get("translated_text", "")))
        if text:
            result = generate_audio_preview(
                text=text,
                language=target_lang,
                audio_format=audio_format,
            )
            results.append(result)

    return results


def save_audio_to_file(audio_result: AudioPreviewResult, filepath: str) -> str:
    """Save audio preview to a file.

    Args:
        audio_result: AudioPreviewResult with base64 audio content.
        filepath: Path to save the audio file.

    Returns:
        Path to the saved file.
    """
    import base64 as b64

    audio_bytes = b64.b64decode(audio_result.audio_content_base64)

    with open(filepath, "wb") as f:
        f.write(audio_bytes)

    return filepath


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        lang = sys.argv[1]
        text = sys.argv[2]
        result = generate_audio_preview(text, lang)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print("Usage: localized_audio_preview.py <language> <text>")
