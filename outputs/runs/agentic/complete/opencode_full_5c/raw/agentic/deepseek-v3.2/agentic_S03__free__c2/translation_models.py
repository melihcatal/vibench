from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class TranslationFormat(Enum):
    """Supported translation formats."""

    TEXT = "text"
    HTML = "html"
    PLAIN = "plain"


@dataclass
class TranslationRequest:
    """Request model for translation operations."""

    text: str
    source_language: str = "en"
    target_language: str = "es"
    format: TranslationFormat = TranslationFormat.TEXT
    preserve_formatting: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        return {
            "q": self.text,
            "source": self.source_language,
            "target": self.target_language,
            "format": self.format.value,
            "model": "nmt",  # Neural Machine Translation model
        }


@dataclass
class TranslationResponse:
    """Response model for translation operations."""

    translated_text: str
    source_language: str
    target_language: str
    detected_source_language: Optional[str] = None
    confidence: Optional[float] = None
    model_used: str = "google-translation-api"

    @classmethod
    def from_api_response(
        cls, api_response: Dict[str, Any], source_lang: str, target_lang: str
    ) -> "TranslationResponse":
        """Create from Google Cloud Translation API response."""
        return cls(
            translated_text=api_response.get("translatedText", ""),
            source_language=source_lang,
            target_language=target_lang,
            detected_source_language=api_response.get("detectedSourceLanguage"),
            model_used="google-translation-api",
        )


@dataclass
class BatchTranslationRequest:
    """Request model for batch translation operations."""

    texts: List[str]
    source_language: str = "en"
    target_language: str = "es"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        return {
            "q": self.texts,
            "source": self.source_language,
            "target": self.target_language,
            "format": "text",
        }


@dataclass
class BatchTranslationResponse:
    """Response model for batch translation operations."""

    translations: List[TranslationResponse]

    @classmethod
    def from_api_responses(
        cls, api_responses: List[Dict[str, Any]], source_lang: str, target_lang: str
    ) -> "BatchTranslationResponse":
        """Create from list of Google Cloud Translation API responses."""
        translations = []
        for api_response in api_responses:
            translations.append(
                TranslationResponse.from_api_response(
                    api_response, source_lang, target_lang
                )
            )
        return cls(translations=translations)


def normalize_text_for_translation(text: str) -> str:
    """Normalize text before translation."""
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Remove extra whitespace but preserve meaningful formatting
    text = " ".join(text.split())

    return text


def validate_language_pair(source_lang: str, target_lang: str) -> bool:
    """Validate that source and target languages are different."""
    if source_lang == target_lang:
        raise ValueError(
            f"Source and target languages cannot be the same: {source_lang}"
        )

    # Basic validation for common language codes
    valid_codes = {"en", "es", "fr", "de", "zh", "ja", "ko", "ru", "ar", "hi"}

    if source_lang not in valid_codes:
        print(f"Warning: Source language code '{source_lang}' may not be supported")

    if target_lang not in valid_codes:
        print(f"Warning: Target language code '{target_lang}' may not be supported")

    return True
