"""
Translation request, response, and normalization helpers for General Text Translation.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    """Represents a single translation request."""
    text: str
    source_lang: Optional[str] = None
    target_lang: str = "en"
    formality: Optional[str] = None
    preserve_formatting: bool = True
    tag_handling: Optional[str] = None
    ignore_tags: Optional[List[str]] = None


@dataclass
class TranslationResult:
    """Represents a single translation result."""
    text: str
    source_lang: str
    target_lang: str
    detected_source_lang: Optional[str] = None
    confidence: Optional[float] = None
    billing_chars: Optional[int] = None


@dataclass
class TranslationResponse:
    """Aggregates multiple translation results."""
    results: List[TranslationResult] = field(default_factory=list)
    total_chars: int = 0

    def add_result(self, result: TranslationResult) -> None:
        self.results.append(result)
        if result.billing_chars is not None:
            self.total_chars += result.billing_chars


@dataclass
class DictionaryTranslationResult:
    """Translation result preserving original dictionary keys."""
    original: Dict[str, str]
    translated: Dict[str, str]
    translations: TranslationResponse


def normalize_language_code(code: str) -> str:
    """Normalize language code to DeepL format (uppercase ISO 639-1)."""
    return code.upper().replace("_", "-")


def detect_text_type(text: str) -> str:
    """Detect whether text is plain, HTML, or XML based on content."""
    import re
    if re.search(r"<[^>]+>", text):
        if re.search(r"<(html|head|body|div|span|p|table|ul|li|form)", text, re.IGNORECASE):
            return "html"
        return "xml"
    return "plain"


def extract_tag_names(text: str) -> List[str]:
    """Extract HTML/XML tag names from text for tag preservation."""
    import re
    tags = re.findall(r"<(/?)(\w+)[^>]*>", text)
    unique_tags = list(set(tag[1] for tag in tags))
    return unique_tags


def build_translation_request(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    content_type: str = "plain"
) -> Dict[str, Any]:
    """Build a DeepL-compatible request dictionary."""
    params: Dict[str, Any] = {
        "target_lang": normalize_language_code(target_lang),
    }
    if source_lang:
        params["source_lang"] = normalize_language_code(source_lang)
    if formality:
        params["formality"] = formality
    if content_type == "html":
        params["tag_handling"] = "html"
        params["preserve_formatting"] = True
    elif content_type == "xml":
        params["tag_handling"] = "xml"
        params["preserve_formatting"] = True
    return params


def parse_translation_response(raw_text: str, request_params: Dict[str, Any]) -> TranslationResult:
    """Parse raw translation text into a TranslationResult."""
    return TranslationResult(
        text=raw_text,
        source_lang=request_params.get("source_lang", "auto"),
        target_lang=request_params["target_lang"],
    )


def validate_language_pair(source_lang: Optional[str], target_lang: str) -> bool:
    """Validate that source and target language pair is supported."""
    valid_languages = {
        "EN", "DE", "FR", "ES", "PT", "IT", "NL", "PL", "RU", "JA", "ZH", "BG",
        "CS", "DA", "EL", "ET", "FI", "HU", "LV", "LT", "RO", "SK", "SL", "SV",
        "UK", "KO", "ID", "TR", "NB",
    }
    target = normalize_language_code(target_lang)
    if target not in valid_languages:
        return False
    if source_lang:
        source = normalize_language_code(source_lang)
        if source not in valid_languages and source != "AUTO":
            return False
    return True
