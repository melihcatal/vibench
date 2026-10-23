from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class TranslationFormat(Enum):
    """Supported translation formats."""

    TEXT = "text"
    HTML = "html"


@dataclass
class TranslationRequest:
    """Request model for translation operations."""

    text: str
    target_language: str
    source_language: Optional[str] = None
    format: TranslationFormat = TranslationFormat.TEXT

    def to_google_params(self) -> Dict[str, Any]:
        """Convert to Google Cloud Translation API parameters."""
        params = {"target_language": self.target_language, "format_": self.format.value}
        if self.source_language:
            params["source_language"] = self.source_language
        return params


@dataclass
class TranslationResponse:
    """Response model for translation operations."""

    translated_text: str
    source_language: Optional[str] = None
    detected_language: Optional[str] = None
    original_text: Optional[str] = None

    @classmethod
    def from_google_result(
        cls, result: Dict[str, Any], original_text: Optional[str] = None
    ) -> "TranslationResponse":
        """Create from Google Cloud Translation API result."""
        return cls(
            translated_text=result["translatedText"],
            source_language=result.get("detectedSourceLanguage"),
            detected_language=result.get("detectedSourceLanguage"),
            original_text=original_text,
        )


@dataclass
class BatchTranslationRequest:
    """Request model for batch translation operations."""

    texts: List[str]
    target_language: str
    source_language: Optional[str] = None
    format: TranslationFormat = TranslationFormat.TEXT


@dataclass
class BatchTranslationResponse:
    """Response model for batch translation operations."""

    translations: List[TranslationResponse]

    @classmethod
    def from_google_results(
        cls, results: List[Dict[str, Any]], original_texts: Optional[List[str]] = None
    ) -> "BatchTranslationResponse":
        """Create from Google Cloud Translation API batch results."""
        translations = []
        for i, result in enumerate(results):
            original_text = original_texts[i] if original_texts else None
            translations.append(
                TranslationResponse.from_google_result(result, original_text)
            )
        return cls(translations=translations)


def normalize_language_code(language_code: str) -> str:
    """Normalize language code to standard format."""
    return language_code.lower().replace("_", "-")


def validate_translation_request(request: TranslationRequest) -> bool:
    """Validate translation request parameters."""
    if not request.text or not request.text.strip():
        return False
    if not request.target_language or len(request.target_language) < 2:
        return False
    return True
