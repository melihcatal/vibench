import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    format: str = "text"
    model: str = "nmt"


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    model: Optional[str] = None


@dataclass
class BatchTranslationRequest:
    texts: list[str]
    source_language: Optional[str] = None
    target_language: str = "en"
    format: str = "text"
    model: str = "nmt"


@dataclass
class BatchTranslationResult:
    results: list[TranslationResult]


@dataclass
class DictionaryTranslationRequest:
    dictionary: dict[str, str]
    source_language: Optional[str] = None
    target_language: str = "en"
    model: str = "nmt"


@dataclass
class DictionaryTranslationResult:
    translated_dictionary: dict[str, str]


@dataclass
class QualityIssue:
    issue_type: str
    severity: str
    description: str
    segment_index: Optional[int] = None


@dataclass
class QualitySummary:
    overall_score: float
    issues: list[QualityIssue]
    source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class UnsafeContentFlag:
    category: str
    confidence: float
    flagged_text: str
    segment_index: Optional[int] = None


@dataclass
class UnsafeContentReport:
    has_unsafe_content: bool
    flags: list[UnsafeContentFlag]


@dataclass
class TranslationEmbedding:
    text: str
    embedding: list[float]
    source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class TranslationMemoryIndex:
    embeddings: list[TranslationEmbedding]
    dimension: int = 768


@dataclass
class AudioPreviewRequest:
    text: str
    language_code: str
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclass
class AudioPreviewResult:
    audio_content: bytes
    audio_format: str = "mp3"
    duration_seconds: Optional[float] = None


def normalize_language_code(lang_code: str) -> str:
    lang_code = lang_code.strip().lower()
    if lang_code in ("zh", "zh-cn"):
        return "zh-CN"
    if lang_code == "zh-tw":
        return "zh-TW"
    if lang_code == "pt":
        return "pt"
    if lang_code == "pt-br":
        return "pt-BR"
    if "-" in lang_code:
        parts = lang_code.split("-", 1)
        return f"{parts[0]}-{parts[1].upper()}"
    return lang_code


def validate_language_code(lang_code: str) -> bool:
    valid_prefixes = {
        "en",
        "es",
        "fr",
        "de",
        "it",
        "pt",
        "ru",
        "ja",
        "ko",
        "zh",
        "ar",
        "hi",
        "bn",
        "pa",
        "te",
        "mr",
        "ta",
        "ur",
        "gu",
        "kn",
        "ml",
        "or",
        "pl",
        "uk",
        "nl",
        "el",
        "cs",
        "sv",
        "fi",
        "da",
        "no",
        "tr",
        "th",
        "vi",
        "id",
        "ms",
        "tl",
        "he",
        "fa",
        "ro",
        "hu",
        "bg",
        "hr",
        "sk",
        "sl",
        "sr",
        "lt",
        "lv",
        "et",
        "is",
        "ga",
        "cy",
        "eu",
        "ca",
        "gl",
        "af",
        "sw",
        "zu",
        "xh",
        "am",
        "ne",
        "si",
        "km",
        "lo",
        "my",
        "ka",
        "hy",
        "az",
        "kk",
        "uz",
        "tk",
        "ky",
        "tg",
        "mn",
        "bo",
        "dz",
        "ti",
        "om",
        "so",
        "mg",
        "ny",
        "sn",
        "st",
        "tn",
        "ts",
        "ve",
        "ss",
        "nr",
        "nso",
    }
    normalized = normalize_language_code(lang_code)
    prefix = normalized.split("-")[0].lower()
    return prefix in valid_prefixes


def parse_google_translate_response(
    response_data: dict, source_text: str
) -> TranslationResult:
    translations = response_data.get("data", {}).get("translations", [])
    if not translations:
        return TranslationResult(translated_text="", detected_source_language=None)
    translation = translations[0]
    translated_text = translation.get("translatedText", "")
    detected_language = translation.get("detectedSourceLanguage")
    model = translation.get("model")
    return TranslationResult(
        translated_text=translated_text,
        detected_source_language=detected_language,
        model=model,
    )


def build_google_translate_payload(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    format_type: str = "text",
    model: str = "nmt",
) -> dict:
    payload: dict = {
        "q": text,
        "target": normalize_language_code(target_language),
        "format": format_type,
        "model": model,
    }
    if source_language:
        payload["source"] = normalize_language_code(source_language)
    return payload


def build_google_tts_payload(
    text: str,
    language_code: str,
    voice_name: Optional[str] = None,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    audio_encoding: str = "MP3",
) -> dict:
    voice_selection: dict = {
        "languageCode": normalize_language_code(language_code),
    }
    if voice_name:
        voice_selection["name"] = voice_name
    payload: dict = {
        "input": {"text": text},
        "voice": voice_selection,
        "audioConfig": {
            "audioEncoding": audio_encoding,
            "speakingRate": speaking_rate,
            "pitch": pitch,
        },
    }
    return payload
