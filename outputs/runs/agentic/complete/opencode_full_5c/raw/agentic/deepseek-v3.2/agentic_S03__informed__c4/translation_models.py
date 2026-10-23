from typing import TypedDict, Optional, List, Dict, Any
from dataclasses import dataclass


class TranslationRequest(TypedDict):
    """Request model for translation operations."""

    text: str
    target_language: str
    source_language: Optional[str]
    format: Optional[str]


class BatchTranslationRequest(TypedDict):
    """Request model for batch translation operations."""

    texts: List[str]
    target_language: str
    source_language: Optional[str]


class DictionaryTranslationRequest(TypedDict):
    """Request model for dictionary translation operations."""

    data: Dict[str, str]
    target_language: str
    source_language: Optional[str]


class TranslationResponse(TypedDict):
    """Response model for translation operations."""

    translated_text: str
    source_language: str
    target_language: str
    original_text: str
    provider: str


class BatchTranslationResponse(TypedDict):
    """Response model for batch translation operations."""

    translated_texts: List[str]
    source_language: str
    target_language: str
    original_texts: List[str]
    provider: str


class DictionaryTranslationResponse(TypedDict):
    """Response model for dictionary translation operations."""

    translated_data: Dict[str, str]
    source_language: str
    target_language: str
    original_data: Dict[str, str]
    provider: str


@dataclass
class LanguagePair:
    """Data class for language pair configuration."""

    source: str
    target: str

    def __str__(self) -> str:
        return f"{self.source}->{self.target}"


@dataclass
class TranslationConfig:
    """Configuration for translation operations."""

    provider: str = "google-cloud-translation"
    default_target: str = "es"
    default_source: str = "en"
    timeout: int = 30
    retry_attempts: int = 3

    @classmethod
    def from_env(cls) -> "TranslationConfig":
        """Create configuration from environment variables."""
        return cls(
            provider=os.environ.get("TRANSLATION_PROVIDER", "google-cloud-translation"),
            default_target=os.environ.get("DEFAULT_TARGET_LANGUAGE", "es"),
            default_source=os.environ.get("DEFAULT_SOURCE_LANGUAGE", "en"),
            timeout=int(os.environ.get("TRANSLATION_TIMEOUT", "30")),
            retry_attempts=int(os.environ.get("TRANSLATION_RETRY_ATTEMPTS", "3")),
        )


def normalize_text_for_translation(text: str) -> str:
    """Normalize text before translation (trim, remove extra whitespace)."""
    return " ".join(text.strip().split())


def normalize_batch_texts(texts: List[str]) -> List[str]:
    """Normalize a list of texts for batch translation."""
    return [normalize_text_for_translation(text) for text in texts]


def parse_google_translation_response(response: Dict[str, Any]) -> TranslationResponse:
    """Parse Google Cloud Translation response into standardized format."""
    return TranslationResponse(
        translated_text=response.get("translatedText", ""),
        source_language=response.get("detectedSourceLanguage", ""),
        target_language=response.get("target", ""),
        original_text=response.get("input", ""),
        provider="google-cloud-translation",
    )


import os
