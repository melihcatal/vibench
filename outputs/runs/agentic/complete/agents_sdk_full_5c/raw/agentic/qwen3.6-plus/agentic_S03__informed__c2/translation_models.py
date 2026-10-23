"""Request, response, and normalization helpers for General Text Translation.

Defines dataclasses for translation requests and responses, along with
utility functions for normalizing language codes and handling response
formats from the DeepL translation API.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TranslationRequest:
    """Normalized translation request parameters."""

    source_text: str
    target_lang: str
    source_lang: str | None = None
    formality: str | None = None
    preserve_formatting: bool = True
    tag_handling: str | None = None
    context: str | None = None
    glossary_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_deepl_kwargs(self) -> dict[str, Any]:
        """Convert request to DeepL SDK keyword arguments."""
        kwargs: dict[str, Any] = {"target_lang": self.target_lang.upper()}
        if self.source_lang:
            kwargs["source_lang"] = self.source_lang.upper()
        if self.formality:
            kwargs["formality"] = self.formality
        if not self.preserve_formatting:
            kwargs["preserve_formatting"] = False
        if self.tag_handling:
            kwargs["tag_handling"] = self.tag_handling
        if self.context:
            kwargs["context"] = self.context
        if self.glossary_id:
            kwargs["glossary_id"] = self.glossary_id
        return kwargs


@dataclass
class TranslationResponse:
    """Normalized translation response."""

    translated_text: str
    source_lang: str
    target_lang: str
    provider: str = "deepl"
    model_id: str = "deepl-free"
    billing_chars: int | None = None
    glossary_used: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_deepl_result(
        cls,
        result: Any,
        target_lang: str,
        provider: str = "deepl",
        model_id: str = "deepl-pro",
    ) -> "TranslationResponse":
        """Create a TranslationResponse from a DeepL TextResult."""
        detected_source = getattr(result, "detected_source_lang", None)
        return cls(
            translated_text=result.text,
            source_lang=detected_source or "auto",
            target_lang=target_lang,
            provider=provider,
            model_id=model_id,
            billing_chars=getattr(result, "billing_chars", None),
        )


def normalize_language_code(code: str) -> str:
    """Normalize a language code to the format expected by DeepL API.

    DeepL uses ISO 639-1 language codes in uppercase (e.g., 'EN', 'ES', 'FR').

    Args:
        code: Raw language code string.

    Returns:
        Normalized uppercase language code.
    """
    code = code.strip().upper()
    # Map common aliases to DeepL codes
    alias_map: dict[str, str] = {
        "ZH": "ZH",
        "ZH-CN": "ZH",
        "ZH-TW": "ZH",
        "PT-BR": "PT-BR",
        "PT-PT": "PT-PT",
        "EN-GB": "EN-GB",
        "EN-US": "EN-US",
        "SR": "SR",
    }
    return alias_map.get(code, code.split("-")[0]) if "-" in code else alias_map.get(code, code)


def validate_language_pair(source_lang: str, target_lang: str) -> tuple[str, str]:
    """Validate that source and target language codes are in correct format.

    Args:
        source_lang: Source language code.
        target_lang: Target language code.

    Returns:
        Tuple of normalized (source, target) language codes.

    Raises:
        ValueError: If either language code is invalid.
    """
    normalized_source = normalize_language_code(source_lang) if source_lang else None
    normalized_target = normalize_language_code(target_lang)

    if not normalized_target:
        raise ValueError("Target language code cannot be empty")

    return normalized_source or "auto", normalized_target


def batch_to_individual(
    texts: list[str],
    target_lang: str,
    source_lang: str | None = None,
) -> list[TranslationRequest]:
    """Convert a batch of texts into individual TranslationRequest objects.

    Args:
        texts: List of source texts.
        target_lang: Target language code for all texts.
        source_lang: Source language code for all texts.

    Returns:
        List of TranslationRequest objects.
    """
    return [
        TranslationRequest(
            source_text=text,
            target_lang=target_lang,
            source_lang=source_lang,
        )
        for text in texts
    ]


def merge_responses(responses: list[TranslationResponse]) -> list[str]:
    """Extract translated text strings from a list of TranslationResponse objects.

    Args:
        responses: List of TranslationResponse objects.

    Returns:
        List of translated text strings in order.
    """
    return [r.translated_text for r in responses]
