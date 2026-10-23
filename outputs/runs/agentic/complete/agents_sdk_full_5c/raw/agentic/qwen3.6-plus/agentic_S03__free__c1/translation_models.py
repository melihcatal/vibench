"""Define local request, response, and normalization helpers for General Text Translation."""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


@dataclass
class TranslationRequest:
    """Request model for translation operations."""
    text: str
    source_lang: str
    target_lang: str
    model: str = "general"
    context: Optional[str] = None
    preserve_formatting: bool = True
    glossary_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class TranslationResponse:
    """Response model for translation operations."""
    translated_text: str
    source_lang: str
    target_lang: str
    model_used: str
    confidence: float = 1.0
    character_count: int = 0
    detected_language: Optional[str] = None
    alternative_translations: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    provider: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class BatchTranslationRequest:
    """Request model for batch translation operations."""
    texts: List[str]
    source_lang: str
    target_lang: str
    model: str = "general"
    preserve_order: bool = True
    glossary_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class BatchTranslationResponse:
    """Response model for batch translation operations."""
    translations: List[TranslationResponse]
    total_characters: int = 0
    failed_indices: List[int] = field(default_factory=list)
    processing_time_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "translations": [t.to_dict() for t in self.translations],
            "total_characters": self.total_characters,
            "failed_indices": self.failed_indices,
            "processing_time_ms": self.processing_time_ms,
        }


def normalize_language_code(code: str) -> str:
    """Normalize language code to standard format.

    Handles variations like 'en-US', 'en_US', 'EN', 'english' -> 'en'.

    Args:
        code: Language code in various formats.

    Returns:
        Normalized ISO 639-1 language code.
    """
    if not code:
        return "auto"

    code = code.strip().lower()

    language_map = {
        "english": "en",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "italian": "it",
        "portuguese": "pt",
        "russian": "ru",
        "japanese": "ja",
        "korean": "ko",
        "chinese": "zh",
        "mandarin": "zh",
        "arabic": "ar",
        "hindi": "hi",
        "bengali": "bn",
        "dutch": "nl",
        "polish": "pl",
        "turkish": "tr",
        "swedish": "sv",
        "danish": "da",
        "norwegian": "no",
        "finnish": "fi",
        "czech": "cs",
        "greek": "el",
        "hebrew": "he",
        "thai": "th",
        "vietnamese": "vi",
        "indonesian": "id",
        "malay": "ms",
        "ukrainian": "uk",
        "romanian": "ro",
        "hungarian": "hu",
    }

    if code in language_map:
        return language_map[code]

    code = code.replace("-", "_").split("_")[0]

    if code == "auto" or code == "detect":
        return "auto"

    return code


def calculate_translation_confidence(
    source_text: str,
    translated_text: str,
    model: str,
) -> float:
    """Calculate a basic confidence score for translation quality.

    Args:
        source_text: Original text.
        translated_text: Translated text.
        model: Translation model used.

    Returns:
        Confidence score between 0 and 1.
    """
    if not source_text or not translated_text:
        return 0.0

    source_len = len(source_text)
    translated_len = len(translated_text)

    if source_len == 0:
        return 1.0

    length_ratio = min(source_len, translated_len) / max(source_len, translated_len)
    length_score = 1.0 - abs(1.0 - length_ratio) * 0.3

    model_scores = {
        "google-nmt": 0.95,
        "deepl-free": 0.90,
        "deepl-pro": 0.95,
        "aws-translate-general": 0.88,
        "azure-translate": 0.90,
    }

    base_confidence = model_scores.get(model, 0.85)

    return min(1.0, base_confidence * length_score)


def truncate_text_for_preview(text: str, max_length: int = 100) -> str:
    """Truncate text for preview display.

    Args:
        text: Text to truncate.
        max_length: Maximum length of preview.

    Returns:
        Truncated text with ellipsis if needed.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def count_tokens_approx(text: str) -> int:
    """Approximate token count for text (rough estimate).

    Args:
        text: Input text.

    Returns:
        Approximate token count.
    """
    words = text.split()
    return max(1, int(len(words) * 1.3) + 1)
