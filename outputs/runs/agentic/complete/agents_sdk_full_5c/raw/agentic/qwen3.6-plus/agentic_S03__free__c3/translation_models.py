"""
translation_models.py - Define local request, response, and normalization helpers
for General Text Translation.

Provider: Google Cloud Translation (translate.googleapis.com)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List


@dataclass
class TranslationRequest:
    """Request model for translation operations."""
    text: str
    source_language: str = "auto"
    target_language: str = "en"
    format_: str = "text"
    model: str = "nmt"

    def to_api_payload(self) -> Dict[str, Any]:
        """Convert to Google Cloud Translation API payload format."""
        return {
            "q": self.text,
            "source": self.source_language if self.source_language != "auto" else None,
            "target": self.target_language,
            "format": self.format_,
            "model": self.model,
        }


@dataclass
class TranslationResponse:
    """Response model for translation operations."""
    translated_text: str
    source_language: str
    target_language: str
    model: str = "nmt"
    provider: str = "google_cloud_translate"
    content_type: str = "text"
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "model": self.model,
            "provider": self.provider,
            "content_type": self.content_type,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }


@dataclass
class BatchTranslationResult:
    """Result model for batch translation operations."""
    responses: List[TranslationResponse]
    total_count: int = 0
    successful_count: int = 0
    failed_count: int = 0
    provider: str = "google_cloud_translate"

    def __post_init__(self):
        if self.total_count == 0:
            self.total_count = len(self.responses)
        if self.successful_count == 0:
            self.successful_count = len(self.responses)


def normalize_language_code(code: str) -> str:
    """
    Normalize language codes to Google Cloud Translation format.

    Google Cloud Translation uses ISO 639-1 (two-letter) codes.

    Args:
        code: Language code to normalize.

    Returns:
        Normalized ISO 639-1 language code.
    """
    code = code.strip().lower()
    # Map common variations
    language_map = {
        "zh-cn": "zh",
        "zh-tw": "zh-TW",
        "en-us": "en",
        "en-gb": "en",
        "pt-br": "pt",
        "es-mx": "es",
    }
    return language_map.get(code, code)


def validate_request(request: TranslationRequest) -> List[str]:
    """
    Validate a translation request before sending to Google Cloud Translation API.

    Args:
        request: TranslationRequest to validate.

    Returns:
        List of validation error messages (empty if valid).
    """
    errors = []
    if not request.text:
        errors.append("Text cannot be empty")
    if not request.target_language:
        errors.append("Target language is required")
    if request.format_ not in ("text", "html"):
        errors.append(f"Invalid format: {request.format_}. Must be 'text' or 'html'")
    return errors
