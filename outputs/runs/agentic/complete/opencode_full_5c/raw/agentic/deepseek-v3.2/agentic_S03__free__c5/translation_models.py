from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class TranslationRequest:
    """Data class for translation request."""

    text: str
    source_lang: str = "en"
    target_lang: str = "es"
    format_type: str = "text"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        return {
            "text": self.text,
            "source_language": self.source_lang,
            "target_language": self.target_lang,
            "format": self.format_type,
        }


@dataclass
class TranslationResponse:
    """Data class for translation response."""

    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    detected_source_lang: Optional[str] = None

    @classmethod
    def from_google_response(
        cls, original_text: str, google_response: Dict[str, Any]
    ) -> "TranslationResponse":
        """Create from Google Cloud Translation API response."""
        return cls(
            original_text=original_text,
            translated_text=google_response.get("translatedText", ""),
            source_lang=google_response.get("detectedSourceLanguage", ""),
            target_lang=google_response.get("target", ""),
            detected_source_lang=google_response.get("detectedSourceLanguage"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "detected_source_lang": self.detected_source_lang,
        }


@dataclass
class BatchTranslationRequest:
    """Data class for batch translation request."""

    texts: List[str]
    source_lang: str = "en"
    target_lang: str = "es"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "texts": self.texts,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
        }


@dataclass
class BatchTranslationResponse:
    """Data class for batch translation response."""

    requests: List[TranslationRequest]
    responses: List[TranslationResponse]

    def get_translated_texts(self) -> List[str]:
        """Get list of translated texts."""
        return [resp.translated_text for resp in self.responses]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "requests": [req.to_dict() for req in self.requests],
            "responses": [resp.to_dict() for resp in self.responses],
        }


def normalize_text_for_translation(text: str) -> str:
    """
    Normalize text before translation.

    Args:
        text: Input text

    Returns:
        Normalized text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = " ".join(text.split())

    return text


def parse_translation_error(error: Exception) -> Dict[str, Any]:
    """
    Parse translation error for better error messages.

    Args:
        error: Exception from translation API

    Returns:
        Dictionary with error details
    """
    error_str = str(error)

    if "quota" in error_str.lower():
        return {
            "type": "quota_exceeded",
            "message": "Translation quota exceeded. Please check your Google Cloud billing.",
            "original_error": error_str,
        }
    elif "credentials" in error_str.lower() or "authentication" in error_str.lower():
        return {
            "type": "authentication_error",
            "message": "Authentication failed. Check your GOOGLE_APPLICATION_CREDENTIALS.",
            "original_error": error_str,
        }
    elif "language" in error_str.lower():
        return {
            "type": "language_error",
            "message": "Invalid language code. Please check language codes.",
            "original_error": error_str,
        }
    else:
        return {
            "type": "unknown_error",
            "message": "Translation failed.",
            "original_error": error_str,
        }
