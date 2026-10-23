import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    formality: Optional[str] = None
    preserve_formatting: bool = True
    tag_handling: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    detected_source_language: Optional[str] = None
    confidence: Optional[float] = None
    character_count: int = 0


@dataclass
class BatchTranslationRequest:
    texts: list[str]
    source_language: str
    target_language: str
    formality: Optional[str] = None
    preserve_formatting: bool = True


@dataclass
class BatchTranslationResponse:
    translations: list[TranslationResponse]
    total_characters: int = 0


@dataclass
class MarkupTranslationRequest:
    markup_text: str
    source_language: str
    target_language: str
    tag_handling: str = "xml"
    ignore_tags: Optional[list[str]] = None
    preserve_formatting: bool = True


@dataclass
class DictionaryTranslationRequest:
    data: dict[str, str]
    source_language: str
    target_language: str
    formality: Optional[str] = None


@dataclass
class TranslationQualitySummary:
    overall_score: float
    issues: list[dict]
    suggestions: list[str]
    model_used: str = "anthropic-claude-3-5-sonnet"


@dataclass
class UnsafeContentResult:
    is_unsafe: bool
    categories: dict[str, float]
    flagged_segments: list[str]
    service: str = "azure-content-safety"


@dataclass
class EmbeddingResult:
    vectors: list[list[float]]
    model: str = "text-embedding-3-large"
    dimensions: int = 1536
    segments: list[str] = field(default_factory=list)


@dataclass
class AudioPreviewResult:
    audio_url: Optional[str] = None
    audio_data: Optional[bytes] = None
    format: str = "mp3"
    voice_id: str = "default"
    service: str = "elevenlabs"


def normalize_language_code(code: str) -> str:
    code = code.strip().lower()
    code_map = {
        "en": "EN",
        "en-us": "EN-US",
        "en-gb": "EN-GB",
        "zh": "ZH",
        "zh-cn": "ZH",
        "zh-tw": "ZH-TW",
        "es": "ES",
        "fr": "FR",
        "de": "DE",
        "ja": "JA",
        "ko": "KO",
        "pt": "PT",
        "pt-br": "PT-BR",
        "ru": "RU",
        "it": "IT",
        "nl": "NL",
        "ar": "AR",
        "hi": "HI",
        "tr": "TR",
        "pl": "PL",
        "sv": "SV",
        "da": "DA",
        "fi": "FI",
        "no": "NB",
        "el": "EL",
        "cs": "CS",
        "ro": "RO",
        "hu": "HU",
        "id": "ID",
        "th": "TH",
        "uk": "UK",
    }
    return code_map.get(code, code.upper())


def build_deepl_request_payload(
    text: str,
    source_lang: str,
    target_lang: str,
    formality: Optional[str] = None,
    tag_handling: Optional[str] = None,
    preserve_formatting: bool = True,
) -> dict:
    payload = {
        "text": text,
        "source_lang": normalize_language_code(source_lang),
        "target_lang": normalize_language_code(target_lang),
        "preserve_formatting": preserve_formatting,
    }
    if formality:
        payload["formality"] = formality.lower()
    if tag_handling:
        payload["tag_handling"] = tag_handling
    return payload


def parse_deepl_response(
    response_data: dict, source_lang: str, target_lang: str
) -> TranslationResponse:
    translations = response_data.get("translations", [])
    if not translations:
        return TranslationResponse(
            translated_text="",
            source_language=source_lang,
            target_language=target_lang,
        )
    first = translations[0]
    return TranslationResponse(
        translated_text=first.get("text", ""),
        source_language=source_lang,
        target_language=target_lang,
        detected_source_language=first.get("detected_source_language"),
        character_count=len(first.get("text", "")),
    )
