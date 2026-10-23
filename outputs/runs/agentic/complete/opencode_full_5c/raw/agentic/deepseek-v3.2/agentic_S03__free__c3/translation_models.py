from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class TranslationFormat(str, Enum):
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

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary for API calls."""
        data = {
            "q": self.text,
            "target": self.target_language,
            "format": self.format.value,
        }
        if self.source_language:
            data["source"] = self.source_language
        return data


@dataclass
class BatchTranslationRequest:
    """Request model for batch translation operations."""

    texts: List[str]
    target_language: str
    source_language: Optional[str] = None
    format: TranslationFormat = TranslationFormat.TEXT

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary for API calls."""
        data = {
            "q": self.texts,
            "target": self.target_language,
            "format": self.format.value,
        }
        if self.source_language:
            data["source"] = self.source_language
        return data


@dataclass
class TranslationResponse:
    """Response model for translation operations."""

    translated_text: str
    source_language: Optional[str] = None
    detected_language: Optional[str] = None
    confidence: Optional[float] = None

    @classmethod
    def from_google_result(cls, result: Dict[str, Any]) -> "TranslationResponse":
        """Create TranslationResponse from Google Cloud Translation API result."""
        return cls(
            translated_text=result["translatedText"],
            source_language=result.get("detectedSourceLanguage"),
            detected_language=result.get("detectedSourceLanguage"),
            confidence=result.get("confidence"),
        )


@dataclass
class BatchTranslationResponse:
    """Response model for batch translation operations."""

    translations: List[TranslationResponse]

    @classmethod
    def from_google_results(
        cls, results: List[Dict[str, Any]]
    ) -> "BatchTranslationResponse":
        """Create BatchTranslationResponse from Google Cloud Translation API results."""
        translations = [
            TranslationResponse.from_google_result(result) for result in results
        ]
        return cls(translations=translations)


def normalize_language_code(language_code: str) -> str:
    """Normalize language code to standard format."""
    return language_code.lower().strip()


def validate_translation_request(request: TranslationRequest) -> bool:
    """Validate translation request parameters."""
    if not request.text or not request.text.strip():
        return False
    if not request.target_language or len(request.target_language) != 2:
        return False
    if request.source_language and len(request.source_language) != 2:
        return False
    return True
