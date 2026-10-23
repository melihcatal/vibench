"""
Local request, response, and normalization helpers for Hosted LLM Inference
and Model-Family Selection using the OpenAI platform.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Iterator
import json


@dataclass
class SummarizeRequest:
    """Request payload for text summarization."""
    text: str
    max_summary_length: int = 300
    style: str = "concise"


@dataclass
class ExtractRequest:
    """Request payload for JSON extraction from text."""
    text: str
    schema_hint: Dict[str, Any] = field(default_factory=dict)
    strict: bool = True


@dataclass
class QARequest:
    """Request payload for context-based question answering."""
    question: str
    context: str
    max_answer_length: int = 500


@dataclass
class StreamRequest:
    """Request payload for streaming completion."""
    prompt: str
    system_instruction: Optional[str] = None
    max_tokens: int = 1024


@dataclass
class SafetyCheckRequest:
    """Request payload for content safety checking."""
    text: str
    check_type: str = "both"  # 'prompt', 'output', or 'both'


@dataclass
class TranslateRequest:
    """Request payload for translation of model output."""
    text: str
    target_language: str = "en"
    source_language: Optional[str] = None


@dataclass
class EmbeddingRequest:
    """Request payload for text embedding."""
    text: str
    encoding_format: str = "float"


@dataclass
class SpokenBriefRequest:
    """Request payload for spoken brief generation."""
    text: str
    voice: str = "alloy"
    target_length_seconds: int = 30


@dataclass
class SummarizeResponse:
    """Response wrapper for summarization."""
    summary: str
    model_used: str
    token_usage: Optional[Dict[str, int]] = None


@dataclass
class ExtractResponse:
    """Response wrapper for JSON extraction."""
    extracted: Dict[str, Any]
    raw_text: Optional[str] = None
    model_used: str = ""
    token_usage: Optional[Dict[str, int]] = None


@dataclass
class QAResponse:
    """Response wrapper for QA."""
    answer: str
    model_used: str
    token_usage: Optional[Dict[str, int]] = None


@dataclass
class StreamResponse:
    """Response wrapper for streaming completion."""
    full_text: str
    chunks: List[str] = field(default_factory=list)
    model_used: str = ""


@dataclass
class SafetyCheckResponse:
    """Response wrapper for safety checks."""
    is_safe: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    flags: List[str] = field(default_factory=list)


@dataclass
class TranslateResponse:
    """Response wrapper for translation."""
    translated_text: str
    source_language: str = ""
    target_language: str = ""
    model_used: str = ""


@dataclass
class EmbeddingResponse:
    """Response wrapper for embeddings."""
    vector: List[float] = field(default_factory=list)
    dimensions: int = 0
    model_used: str = ""


@dataclass
class SpokenBriefResponse:
    """Response wrapper for spoken brief."""
    audio_bytes: Optional[bytes] = None
    audio_url: Optional[str] = None
    model_used: str = ""
    voice_used: str = ""


def normalize_extracted_json(raw_text: str, schema_hint: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Parse and normalize extracted JSON from an LLM response.

    Strips markdown code fences if present and validates against schema_hint keys.
    """
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    parsed = json.loads(cleaned)

    if schema_hint and isinstance(parsed, dict):
        result = {}
        for key in schema_hint:
            if key in parsed:
                result[key] = parsed[key]
            else:
                result[key] = None
        return result

    return parsed


def build_chat_messages_from_request(
    system_content: str,
    user_content: str,
) -> List[Dict[str, str]]:
    """Build a list of message dicts for OpenAI chat API."""
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]


def extract_text_from_openai_response(completion: Any) -> str:
    """
    Extract the text content from an OpenAI chat completion response.
    Handles both sync and async response objects.
    """
    if hasattr(completion, "choices") and completion.choices:
        message = completion.choices[0].message
        if hasattr(message, "content") and message.content:
            return message.content
    return ""


def extract_token_usage(completion: Any) -> Optional[Dict[str, int]]:
    """Extract token usage from an OpenAI completion response."""
    if hasattr(completion, "usage") and completion.usage:
        return {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens,
        }
    return None
