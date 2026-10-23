from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class TranslationRequest:
    text: str
    source_lang: str = "EN"
    target_lang: str = "ES"
    preserve_formatting: bool = True
    tag_handling: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    source_lang: str
    target_lang: str
    character_count: int
    confidence: Optional[float] = None


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_lang: str = "EN"
    target_lang: str = "ES"


@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]
    total_characters: int


@dataclass
class QualityIssue:
    issue_type: str
    severity: str
    description: str
    segment_index: Optional[int] = None


@dataclass
class QualitySummary:
    overall_score: float
    issues: List[QualityIssue]
    character_count: int
    language_pair: str


@dataclass
class UnsafeContentFlag:
    content_type: str
    severity: str
    matched_text: str
    segment_index: int
    category_scores: Optional[Dict[str, float]] = None


@dataclass
class UnsafeContentReport:
    flags: List[UnsafeContentFlag]
    is_safe: bool
    total_segments: int
    provider: str = "openai"


@dataclass
class EmbeddingSegment:
    text: str
    embedding: List[float]
    source_lang: str
    target_lang: str
    segment_id: str


@dataclass
class TranslationMemoryIndex:
    segments: List[EmbeddingSegment]
    index_name: str
    embedding_model: str
    dimension: int


@dataclass
class AudioPreviewRequest:
    text: str
    language: str
    voice_id: Optional[str] = None
    speed: float = 1.0


@dataclass
class AudioPreviewResponse:
    audio_url: str
    language: str
    duration_seconds: float
    voice_id: str
    model: str


def normalize_language_code(lang: str) -> str:
    lang_upper = lang.upper()
    code_map = {
        "EN": "EN",
        "EN-US": "EN-US",
        "EN-GB": "EN-GB",
        "ES": "ES",
        "FR": "FR",
        "DE": "DE",
        "IT": "IT",
        "PT": "PT",
        "PT-BR": "PT-BR",
        "JA": "JA",
        "ZH": "ZH",
        "ZH-HANS": "ZH",
        "KO": "KO",
        "RU": "RU",
        "AR": "AR",
        "NL": "NL",
        "PL": "PL",
        "SV": "SV",
    }
    return code_map.get(lang_upper, lang_upper)


def normalize_response_text(text: str) -> str:
    return text.strip()


def calculate_character_count(texts: list) -> int:
    return sum(len(t) for t in texts if isinstance(t, str))
