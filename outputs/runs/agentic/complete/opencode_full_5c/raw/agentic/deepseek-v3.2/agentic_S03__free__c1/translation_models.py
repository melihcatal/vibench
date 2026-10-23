from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class TranslationModel(str, Enum):
    """Translation models available in Google Cloud Translation API."""

    NMT = "nmt"  # Neural Machine Translation
    BASE = "base"  # Phrase-Based Machine Translation


class TranslationFormat(str, Enum):
    """Supported translation formats."""

    TEXT = "text"
    HTML = "html"


@dataclass
class TranslationRequest:
    """Request model for single text translation."""

    text: str
    source_lang: str = "auto"
    target_lang: str = "en"
    model: TranslationModel = TranslationModel.NMT
    format: TranslationFormat = TranslationFormat.TEXT


@dataclass
class TranslationResponse:
    """Response model for single text translation."""

    translated_text: str
    source_lang: str
    target_lang: str
    model_used: TranslationModel
    confidence: Optional[float] = None


@dataclass
class BatchTranslationRequest:
    """Request model for batch translation."""

    texts: List[str]
    source_lang: str = "auto"
    target_lang: str = "en"
    model: TranslationModel = TranslationModel.NMT


@dataclass
class BatchTranslationResponse:
    """Response model for batch translation."""

    translated_texts: List[str]
    source_lang: str
    target_lang: str
    model_used: TranslationModel


@dataclass
class MarkupTranslationRequest:
    """Request model for markup translation."""

    markup_content: str
    source_lang: str = "auto"
    target_lang: str = "en"
    model: TranslationModel = TranslationModel.NMT
    format: TranslationFormat = TranslationFormat.HTML


@dataclass
class MarkupTranslationResponse:
    """Response model for markup translation."""

    translated_markup: str
    source_lang: str
    target_lang: str
    model_used: TranslationModel


@dataclass
class DictionaryTranslationRequest:
    """Request model for dictionary translation."""

    data: Dict[str, Any]
    source_lang: str = "auto"
    target_lang: str = "en"
    model: TranslationModel = TranslationModel.NMT
    translate_only_strings: bool = True


@dataclass
class DictionaryTranslationResponse:
    """Response model for dictionary translation."""

    translated_data: Dict[str, Any]
    source_lang: str
    target_lang: str
    model_used: TranslationModel


def normalize_text_for_translation(text: str) -> str:
    """Normalize text before translation."""
    if not text:
        return text
    return text.strip()


def parse_google_translation_response(response: Dict) -> Dict[str, Any]:
    """Parse Google Cloud Translation API response."""
    return {
        "translated_text": response.get("translatedText", ""),
        "source_lang": response.get("detectedSourceLanguage", "unknown"),
        "input": response.get("input", ""),
        "model": response.get("model", "nmt"),
    }
