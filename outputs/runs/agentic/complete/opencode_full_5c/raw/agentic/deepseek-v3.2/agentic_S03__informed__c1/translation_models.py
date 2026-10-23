from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class TranslationFormat(str, Enum):
    """Supported translation formats."""

    TEXT = "text"
    HTML = "html"
    PLAIN = "plain"


@dataclass
class TranslationRequest:
    """Request model for translation operations."""

    text: str
    target_language: str = "en"
    source_language: Optional[str] = None
    format: TranslationFormat = TranslationFormat.TEXT

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        result = {"target_language": self.target_language, "values": self.text}
        if self.source_language:
            result["source_language"] = self.source_language
        if self.format == TranslationFormat.HTML:
            result["format_"] = "html"
        return result


@dataclass
class TranslationResponse:
    """Response model for translation operations."""

    translated_text: str
    source_language: Optional[str]
    target_language: str
    input_text: str
    format: TranslationFormat = TranslationFormat.TEXT

    @classmethod
    def from_google_result(
        cls,
        result: Dict[str, Any],
        input_text: str,
        target_language: str,
        format: TranslationFormat = TranslationFormat.TEXT,
    ) -> "TranslationResponse":
        """Create from Google Cloud Translation result."""
        return cls(
            translated_text=result["translatedText"],
            source_language=result.get("detectedSourceLanguage"),
            target_language=target_language,
            input_text=input_text,
            format=format,
        )


@dataclass
class BatchTranslationRequest:
    """Request model for batch translation operations."""

    texts: List[str]
    target_language: str = "en"
    source_language: Optional[str] = None
    format: TranslationFormat = TranslationFormat.TEXT

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        result = {"target_language": self.target_language, "values": self.texts}
        if self.source_language:
            result["source_language"] = self.source_language
        if self.format == TranslationFormat.HTML:
            result["format_"] = "html"
        return result


@dataclass
class BatchTranslationResponse:
    """Response model for batch translation operations."""

    items: List[TranslationResponse]

    @classmethod
    def from_google_results(
        cls,
        results: List[Dict[str, Any]],
        texts: List[str],
        target_language: str,
        format: TranslationFormat = TranslationFormat.TEXT,
    ) -> "BatchTranslationResponse":
        """Create from Google Cloud Translation batch results."""
        items = []
        for i, result in enumerate(results):
            items.append(
                TranslationResponse.from_google_result(
                    result, texts[i], target_language, format
                )
            )
        return cls(items=items)


def normalize_text_for_translation(text: str) -> str:
    """Normalize text for translation by removing extra whitespace."""
    return " ".join(text.strip().split())


def validate_translation_result(result: Dict[str, Any]) -> bool:
    """Validate that a translation result has required fields."""
    required = ["translatedText", "target_language", "input_text"]
    return all(key in result for key in required)


def extract_translation_metadata(result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract metadata from translation result."""
    return {
        "source_language": result.get("detectedSourceLanguage"),
        "confidence": result.get("confidence"),
        "model": result.get("model", "nmt"),  # Google's Neural Machine Translation
    }
