"""
Define local request, response, and normalization helpers for General Text Translation.
Provides data structures and utility functions for translation payloads.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime
import re


@dataclass
class TranslationRequest:
    """Standardized translation request model."""
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    format_type: str = "text"
    model: str = "nmt"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary representation."""
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class TranslationResult:
    """Single translation result."""
    translated_text: str
    source_language: str
    target_language: str
    original_text: str
    confidence: float = 1.0
    model_used: str = ""


@dataclass
class TranslationResponse:
    """Standardized translation response model."""
    results: List[TranslationResult] = field(default_factory=list)
    success: bool = True
    error_message: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    @property
    def translated_texts(self) -> List[str]:
        """Extract list of translated texts from results."""
        return [r.translated_text for r in self.results]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary representation."""
        return {
            "results": [asdict(r) for r in self.results],
            "success": self.success,
            "error_message": self.error_message,
            "request_id": self.request_id,
            "timestamp": self.timestamp,
        }


@dataclass
class BatchTranslationRequest:
    """Batch translation request model."""
    texts: List[str]
    source_language: Optional[str] = None
    target_language: str = "en"
    format_type: str = "text"
    preserve_order: bool = True


@dataclass
class MarkupTranslationRequest:
    """Markup/HTML translation request model."""
    markup_text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    tag_pattern: str = r"<[^>]+>"


@dataclass
class DictionaryTranslationRequest:
    """Dictionary translation request model."""
    dictionary: Dict[str, str]
    source_language: Optional[str] = None
    target_language: str = "en"


@dataclass
class QualityIssue:
    """Translation quality issue record."""
    segment: str
    issue_type: str
    severity: str
    description: str
    score: float = 0.0


@dataclass
class QualitySummary:
    """Aggregated translation quality summary."""
    overall_score: float
    total_segments: int
    issues: List[QualityIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def normalize_language_code(code: str) -> str:
    """
    Normalize language code to ISO 639-1 format.
    
    Args:
        code: Language code string (e.g., 'en-US', 'zh-CN', 'en').
    
    Returns:
        Normalized language code (e.g., 'en', 'zh').
    """
    if not code:
        return "en"
    
    code = code.strip().lower()
    
    if "-" in code:
        return code.split("-")[0]
    
    if "_" in code:
        return code.split("_")[0]
    
    return code


def split_markup_into_segments(
    markup_text: str,
    tag_pattern: str = r"<[^>]+>",
) -> List[Dict[str, Any]]:
    """
    Split markup text into translatable text segments and tag placeholders.
    
    Args:
        markup_text: HTML or markup text to split.
        tag_pattern: Regex pattern for matching tags.
    
    Returns:
        List of segment dicts with 'type' ('text' or 'tag') and 'content'.
    """
    segments = []
    last_end = 0
    
    for match in re.finditer(tag_pattern, markup_text):
        start, end = match.span()
        
        if start > last_end:
            text_content = markup_text[last_end:start].strip()
            if text_content:
                segments.append({"type": "text", "content": text_content})
        
        segments.append({"type": "tag", "content": match.group(0)})
        last_end = end
    
    remaining = markup_text[last_end:].strip()
    if remaining:
        segments.append({"type": "text", "content": remaining})
    
    return segments


def reassemble_markup(
    segments: List[Dict[str, Any]],
) -> str:
    """
    Reassemble segments back into markup text.
    
    Args:
        segments: List of segment dicts from split_markup_into_segments.
    
    Returns:
        Reassembled markup string.
    """
    return "".join(seg["content"] for seg in segments)


def extract_dictionary_values(
    dictionary: Dict[str, str],
) -> List[str]:
    """
    Extract values from dictionary for batch translation.
    
    Args:
        dictionary: Dictionary with string values to translate.
    
    Returns:
        List of dictionary values.
    """
    return [v for v in dictionary.values() if isinstance(v, str) and v.strip()]


def rebuild_translated_dictionary(
    original_dict: Dict[str, str],
    translated_values: List[str],
) -> Dict[str, str]:
    """
    Rebuild dictionary with translated values, preserving original keys.
    
    Args:
        original_dict: Original dictionary with keys to preserve.
        translated_values: List of translated values in order.
    
    Returns:
        New dictionary with translated values.
    """
    rebuild_dict = {}
    value_idx = 0
    
    for key, value in original_dict.items():
        if isinstance(value, str) and value.strip():
            if value_idx < len(translated_values):
                rebuild_dict[key] = translated_values[value_idx]
                value_idx += 1
            else:
                rebuild_dict[key] = value
        else:
            rebuild_dict[key] = value
    
    return rebuild_dict


def sanitize_text_for_translation(text: str) -> str:
    """
    Sanitize text before sending to translation API.
    
    Args:
        text: Raw input text.
    
    Returns:
        Sanitized text safe for translation.
    """
    if not text:
        return ""
    
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    
    return text
