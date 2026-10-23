from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class TranslationProvider(Enum):
    """Supported translation providers."""

    GOOGLE = "google"
    AWS = "aws"
    DEEPL = "deepl"
    AZURE = "azure"
    ALIBABA = "alibaba"


@dataclass
class TranslationRequest:
    """Request model for translation operations."""

    text: Optional[str] = None
    texts: Optional[List[str]] = None
    target_language: str
    source_language: Optional[str] = None
    provider: TranslationProvider = TranslationProvider.GOOGLE
    options: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate request."""
        if not self.text and not self.texts:
            raise ValueError("Either 'text' or 'texts' must be provided")

        if self.text and self.texts:
            raise ValueError("Only one of 'text' or 'texts' should be provided")


@dataclass
class TranslationResponse:
    """Response model for translation operations."""

    translated_text: Optional[str] = None
    translated_texts: Optional[List[str]] = None
    source_language: Optional[str] = None
    target_language: str
    provider: str
    detected_source_language: Optional[str] = None
    confidence: Optional[float] = None
    raw_response: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Validate response."""
        if not self.translated_text and not self.translated_texts:
            raise ValueError(
                "Either 'translated_text' or 'translated_texts' must be provided"
            )


@dataclass
class BatchTranslationResult:
    """Result model for batch translation operations."""

    translations: List[TranslationResponse]
    failed_indices: List[int] = field(default_factory=list)
    total_processed: int = 0
    total_succeeded: int = 0


def normalize_google_response(response: Dict[str, Any]) -> TranslationResponse:
    """Normalize Google Cloud Translation API response."""
    if isinstance(response, list):
        # Batch response
        translated_texts = [item["translatedText"] for item in response]
        detected_lang = response[0].get("detectedSourceLanguage") if response else None
        return TranslationResponse(
            translated_texts=translated_texts,
            source_language=detected_lang,
            target_language=response[0].get("target", "") if response else "",
            provider="google",
            detected_source_language=detected_lang,
            raw_response=response,
        )
    else:
        # Single response
        return TranslationResponse(
            translated_text=response["translatedText"],
            source_language=response.get("detectedSourceLanguage"),
            target_language=response.get("target", ""),
            provider="google",
            detected_source_language=response.get("detectedSourceLanguage"),
            raw_response=response,
        )


def normalize_aws_response(response: Dict[str, Any]) -> TranslationResponse:
    """Normalize Amazon Translate API response."""
    if "TranslatedTextList" in response:
        # Batch response
        return TranslationResponse(
            translated_texts=response["TranslatedTextList"],
            source_language=response.get("SourceLanguageCode"),
            target_language=response.get("TargetLanguageCode", ""),
            provider="aws",
            raw_response=response,
        )
    else:
        # Single response
        return TranslationResponse(
            translated_text=response["TranslatedText"],
            source_language=response.get("SourceLanguageCode"),
            target_language=response.get("TargetLanguageCode", ""),
            provider="aws",
            raw_response=response,
        )


def normalize_deepl_response(response: Any) -> TranslationResponse:
    """Normalize DeepL API response."""
    if isinstance(response, list):
        # Batch response
        translated_texts = [item.text for item in response]
        detected_lang = response[0].detected_source_lang if response else None
        return TranslationResponse(
            translated_texts=translated_texts,
            source_language=detected_lang,
            target_language=response[0].target_lang if response else "",
            provider="deepl",
            detected_source_language=detected_lang,
            raw_response=[item.__dict__ for item in response] if response else [],
        )
    else:
        # Single response
        return TranslationResponse(
            translated_text=response.text,
            source_language=response.detected_source_lang,
            target_language=response.target_lang,
            provider="deepl",
            detected_source_language=response.detected_source_lang,
            raw_response=response.__dict__,
        )


def normalize_azure_response(response: Any) -> TranslationResponse:
    """Normalize Azure AI Translator response."""
    # Azure response structure varies by SDK version
    # This is a simplified normalization
    if hasattr(response, "translations"):
        # Batch response
        translated_texts = [translation.text for translation in response.translations]
        return TranslationResponse(
            translated_texts=translated_texts,
            target_language=response.translations[0].to
            if response.translations
            else "",
            provider="azure",
            raw_response=response.__dict__,
        )
    else:
        # Single response or other format
        return TranslationResponse(
            translated_text=str(response),
            provider="azure",
            raw_response=response.__dict__
            if hasattr(response, "__dict__")
            else response,
        )
