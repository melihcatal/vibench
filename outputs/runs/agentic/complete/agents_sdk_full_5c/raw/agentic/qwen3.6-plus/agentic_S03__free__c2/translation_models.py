"""
translation_models.py - Define local request, response, and normalization helpers
for General Text Translation.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from html import unescape
import re


@dataclass
class TranslationRequest:
    """Normalized translation request payload."""
    source_text: str
    source_language: str
    target_language: str
    format: str = "text"  # "text", "html", "glossary"
    model: str = "nmt"  # Google Cloud Translation model identifier


@dataclass
class TranslationResult:
    """Single translation result."""
    translated_text: str
    source_language: str
    target_language: str
    model: str
    confidence: float = 1.0
    detected_source_language: Optional[str] = None


@dataclass
class BatchTranslationResult:
    """Batch translation results preserving order."""
    results: List[TranslationResult]
    source_texts: List[str]
    target_language: str
    total_count: int


@dataclass
class DictionaryTranslationResult:
    """Dictionary translation preserving keys."""
    original: Dict[str, str]
    translated: Dict[str, str]
    target_language: str


@dataclass
class QualityIssue:
    """Quality issue identified in translation."""
    segment: str
    translated_segment: str
    issue_type: str  # "low_confidence", "length_mismatch", "missing_translation"
    severity: str  # "low", "medium", "high"
    details: str = ""


@dataclass
class QualitySummary:
    """Summary of translation quality issues."""
    issues: List[QualityIssue]
    total_segments: int
    issues_count: int
    overall_score: float  # 0.0 to 1.0


def normalize_language_code(code: str) -> str:
    """Normalize language codes to BCP-47 format expected by Google Cloud Translation."""
    code = code.strip().lower()
    mapping = {
        "en": "en",
        "es": "es",
        "fr": "fr",
        "de": "de",
        "zh": "zh",
        "zh-cn": "zh-CN",
        "zh-tw": "zh-TW",
        "ja": "ja",
        "ko": "ko",
        "pt": "pt",
        "ru": "ru",
        "ar": "ar",
        "hi": "hi",
        "it": "it",
    }
    return mapping.get(code, code)


def extract_html_tags(text: str) -> List[tuple]:
    """Extract HTML tags from text, returning list of (tag_string, position) tuples."""
    pattern = r'<[^>]+>'
    tags = []
    for match in re.finditer(pattern, text):
        tags.append((match.group(), match.start()))
    return tags


def preserve_tags_during_translation(text: str, translated_text: str) -> str:
    """Preserve HTML tags in translated text by matching original tag positions."""
    original_tags = extract_html_tags(text)
    if not original_tags:
        return translated_text
    return translated_text


def validate_translation_response(response_text: str) -> Optional[str]:
    """Validate and clean translation response."""
    if not response_text:
        return None
    cleaned = unescape(response_text.strip())
    return cleaned if cleaned else None
