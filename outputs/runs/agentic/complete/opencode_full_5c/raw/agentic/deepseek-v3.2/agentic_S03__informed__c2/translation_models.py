from typing import Dict, List, Any, Optional
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
    target_language: str = "en"
    source_language: Optional[str] = None
    format: TranslationFormat = TranslationFormat.TEXT

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        result = {
            "q": self.text,
            "target": self.target_language,
            "format": self.format.value,
        }
        if self.source_language:
            result["source"] = self.source_language
        return result


@dataclass
class BatchTranslationRequest:
    """Request model for batch translation operations."""

    texts: List[str]
    target_language: str = "en"
    source_language: Optional[str] = None
    format: TranslationFormat = TranslationFormat.TEXT

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        result = {
            "q": self.texts,
            "target": self.target_language,
            "format": self.format.value,
        }
        if self.source_language:
            result["source"] = self.source_language
        return result


@dataclass
class TranslationResponse:
    """Response model for translation operations."""

    translated_text: str
    source_language: Optional[str] = None
    detected_source_language: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

    @classmethod
    def from_google_response(cls, response: Dict[str, Any]) -> "TranslationResponse":
        """Create from Google Cloud Translation response."""
        return cls(
            translated_text=response.get("translatedText", ""),
            source_language=response.get("detectedSourceLanguage"),
            detected_source_language=response.get("detectedSourceLanguage"),
            raw_response=response,
        )


@dataclass
class BatchTranslationResponse:
    """Response model for batch translation operations."""

    translations: List[TranslationResponse]
    raw_responses: List[Dict[str, Any]]

    @classmethod
    def from_google_responses(
        cls, responses: List[Dict[str, Any]]
    ) -> "BatchTranslationResponse":
        """Create from Google Cloud Translation batch responses."""
        translations = [
            TranslationResponse.from_google_response(resp) for resp in responses
        ]
        return cls(translations=translations, raw_responses=responses)

    def get_translated_texts(self) -> List[str]:
        """Get list of translated texts."""
        return [t.translated_text for t in self.translations]


def normalize_text_for_translation(text: str, max_length: int = 5000) -> str:
    """
    Normalize text for translation.

    Args:
        text: Text to normalize
        max_length: Maximum length to truncate to

    Returns:
        Normalized text
    """
    if not text:
        return ""

    text = text.strip()

    if len(text) > max_length:
        text = text[:max_length] + "..."

    return text


def split_long_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    """
    Split long text into chunks for translation.

    Args:
        text: Text to split
        max_chunk_size: Maximum size of each chunk

    Returns:
        List of text chunks
    """
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    sentences = text.split(". ")
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 2 <= max_chunk_size:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
