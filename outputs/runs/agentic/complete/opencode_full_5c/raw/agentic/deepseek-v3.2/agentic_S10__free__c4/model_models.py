from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from enum import Enum


class ModelFamily(Enum):
    """Supported model families."""

    GPT4 = "gpt-4"
    GPT4O = "gpt-4o"
    GPT4O_MINI = "gpt-4o-mini"
    GPT35_TURBO = "gpt-3.5-turbo"


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
    model_used: str
    tokens_used: Optional[int] = None


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
    model_used: str
    tokens_used: Optional[int] = None


@dataclass
class QARequest:
    """Request for question answering with context."""

    question: str
    context: str
    model: Optional[str] = None
    temperature: float = 0.2


@dataclass
class QAResponse:
    """Response from question answering."""

    answer: str
    model_used: str
    tokens_used: Optional[int] = None


@dataclass
class StreamRequest:
    """Request for streaming completion."""

    prompt: str
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 500


@dataclass
class StreamChunk:
    """Chunk from streaming completion."""

    content: str
    is_final: bool = False


def normalize_model_name(model_name: str) -> str:
    """Normalize model name to ensure compatibility."""
    model_name = model_name.lower()
    if "gpt-4o-mini" in model_name:
        return "gpt-4o-mini"
    elif "gpt-4o" in model_name:
        return "gpt-4o"
    elif "gpt-4" in model_name:
        return "gpt-4"
    elif "gpt-3.5" in model_name:
        return "gpt-3.5-turbo"
    return model_name


def get_model_family(model_name: str) -> ModelFamily:
    """Get model family from model name."""
    normalized = normalize_model_name(model_name)
    if normalized == "gpt-4o-mini":
        return ModelFamily.GPT4O_MINI
    elif normalized == "gpt-4o":
        return ModelFamily.GPT4O
    elif normalized == "gpt-4":
        return ModelFamily.GPT4
    elif normalized == "gpt-3.5-turbo":
        return ModelFamily.GPT35_TURBO
    else:
        raise ValueError(f"Unknown model family for: {model_name}")
