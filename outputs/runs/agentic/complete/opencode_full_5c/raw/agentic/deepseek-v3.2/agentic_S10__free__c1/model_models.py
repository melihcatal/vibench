from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """Types of LLM tasks."""

    SUMMARIZATION = "summarization"
    EXTRACTION = "extraction"
    QA = "qa"
    STREAMING = "streaming"
    SAFETY = "safety"
    TRANSLATION = "translation"
    EMBEDDING = "embedding"
    TTS = "tts"


@dataclass
class SummaryRequest:
    """Request for text summarization."""

    text: str
    max_length: int = 200
    model: Optional[str] = None
    temperature: float = 0.3


@dataclass
class SummaryResponse:
    """Response from text summarization."""

    summary: str
    original_length: int
    summary_length: int
    model_used: str


@dataclass
class ExtractRequest:
    """Request for JSON extraction."""

    text: str
    schema: Dict[str, Any]
    model: Optional[str] = None
    temperature: float = 0.1


@dataclass
class ExtractResponse:
    """Response from JSON extraction."""

    extracted_data: Dict[str, Any]
    is_valid: bool
    validation_errors: List[str]
    model_used: str


@dataclass
class QARequest:
    """Request for question answering."""

    question: str
    context: str
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 500


@dataclass
class QAResponse:
    """Response from question answering."""

    answer: str
    confidence: Optional[float] = None
    sources_used: List[str] = None
    model_used: str = ""


@dataclass
class StreamRequest:
    """Request for streaming completion."""

    prompt: str
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 500


@dataclass
class StreamResponse:
    """Response from streaming completion."""

    full_text: str
    chunks: List[str]
    model_used: str


def normalize_text(text: str) -> str:
    """
    Normalize text for LLM processing.

    Args:
        text: Input text

    Returns:
        Normalized text
    """
    if not text:
        return ""

    # Basic normalization
    normalized = text.strip()

    # Remove excessive whitespace
    import re

    normalized = re.sub(r"\s+", " ", normalized)

    return normalized


def validate_json_schema(schema: Dict[str, Any]) -> bool:
    """
    Validate JSON schema structure.

    Args:
        schema: JSON schema to validate

    Returns:
        True if schema is valid
    """
    if not isinstance(schema, dict):
        return False

    # Check for required schema properties
    if "type" not in schema:
        return False

    return True


def calculate_token_estimate(text: str) -> int:
    """
    Estimate token count for text.

    Args:
        text: Input text

    Returns:
        Estimated token count
    """
    # Rough estimate: 1 token ≈ 4 characters for English text
    return len(text) // 4


def format_context_for_qa(context: str, max_tokens: int = 4000) -> str:
    """
    Format context for question answering, truncating if necessary.

    Args:
        context: Original context
        max_tokens: Maximum tokens to allow

    Returns:
        Formatted context
    """
    normalized = normalize_text(context)
    estimated_tokens = calculate_token_estimate(normalized)

    if estimated_tokens <= max_tokens:
        return normalized

    # Truncate to fit within token limit
    chars_to_keep = max_tokens * 4
    truncated = normalized[:chars_to_keep]

    # Try to end at a sentence boundary
    last_period = truncated.rfind(". ")
    if last_period > chars_to_keep * 0.8:  # If we can find a reasonable sentence end
        return truncated[: last_period + 1]

    return truncated + "..."
