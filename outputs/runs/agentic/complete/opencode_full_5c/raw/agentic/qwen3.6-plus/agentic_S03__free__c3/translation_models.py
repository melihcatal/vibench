import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class TranslationRequest:
    text: str
    source_language: str = "auto"
    target_language: str = "en"
    preserve_formatting: bool = False
    context: Optional[str] = None
    custom_instructions: Optional[str] = None


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str = "auto"
    target_language: str = "en"
    preserve_formatting: bool = False
    context: Optional[str] = None


@dataclass
class MarkupTranslationRequest:
    markup: str
    source_language: str = "auto"
    target_language: str = "en"
    tag_types: List[str] = field(default_factory=lambda: ["html", "xml", "markdown"])


@dataclass
class DictionaryTranslationRequest:
    data: Dict[str, Any]
    source_language: str = "auto"
    target_language: str = "en"
    translate_keys: bool = False


@dataclass
class TranslationResult:
    translated_text: str
    source_language_detected: str
    target_language: str
    confidence: float = 1.0
    character_count: int = 0
    word_count: int = 0


@dataclass
class BatchTranslationResult:
    results: List[TranslationResult]
    total_characters: int = 0
    total_words: int = 0


@dataclass
class QualitySummary:
    overall_score: float
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    language_pair: str
    segment_count: int


@dataclass
class SafetyCheckResult:
    is_safe: bool
    flagged_segments: List[Dict[str, Any]]
    risk_level: str
    categories: List[str]


@dataclass
class EmbeddingResult:
    vectors: List[List[float]]
    segment_ids: List[str]
    model_used: str
    dimensions: int


@dataclass
class AudioPreviewResult:
    audio_url: str
    duration_seconds: float
    format: str
    text_preview: str


def normalize_language_code(code: str) -> str:
    code = code.strip().lower()
    language_map = {
        "en": "en",
        "english": "en",
        "eng": "en",
        "es": "es",
        "spanish": "es",
        "spa": "es",
        "fr": "fr",
        "french": "fr",
        "fra": "fr",
        "de": "de",
        "german": "de",
        "deu": "de",
        "ja": "ja",
        "japanese": "ja",
        "jpn": "ja",
        "zh": "zh",
        "chinese": "zh",
        "zho": "zh",
        "zh-cn": "zh",
        "ko": "ko",
        "korean": "ko",
        "kor": "ko",
        "pt": "pt",
        "portuguese": "pt",
        "por": "pt",
        "ru": "ru",
        "russian": "ru",
        "rus": "ru",
        "it": "it",
        "italian": "it",
        "ita": "it",
        "ar": "ar",
        "arabic": "ar",
        "ara": "ar",
        "hi": "hi",
        "hindi": "hi",
        "hin": "hi",
    }
    return language_map.get(code, code)


def count_words(text: str) -> int:
    return len(text.split())


def count_characters(text: str) -> int:
    return len(text)
