"""
Local request, response, and normalization helpers for Hosted LLM Inference
and Model-Family Selection using the Mistral AI platform.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


MISTRAL_MODEL_FAMILIES: Dict[str, List[str]] = {
    "mistral-small": ["mistral-small-latest"],
    "mistral-medium": ["mistral-medium-latest"],
    "mistral-large": ["mistral-large-latest"],
    "open-mistral-nemo": ["open-mistral-nemo-latest"],
    "codestral": ["codestral-latest"],
}

DEFAULT_MISTRAL_MODEL = "mistral-small-latest"


@dataclass
class LLMRequest:
    """Normalized request structure for LLM operations."""
    prompt: str
    system_prompt: Optional[str] = None
    model: str = DEFAULT_MISTRAL_MODEL
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 1.0
    stop_sequences: Optional[List[str]] = None
    stream: bool = False

    def to_mistral_messages(self) -> List[Dict[str, str]]:
        """Convert to Mistral Messages API message format."""
        messages: List[Dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})
        return messages

    def to_mistral_payload(self) -> Dict[str, Any]:
        """Build a complete Mistral Chat API request payload."""
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": self.to_mistral_messages(),
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": self.stream,
        }
        if self.stop_sequences:
            payload["stop"] = self.stop_sequences
        return payload


@dataclass
class LLMResponse:
    """Normalized response structure for LLM operations."""
    content: str
    model: str
    usage_prompt_tokens: int = 0
    usage_completion_tokens: int = 0
    usage_total_tokens: int = 0
    finish_reason: Optional[str] = None
    raw_response: Optional[Any] = None

    @classmethod
    def from_mistral(cls, chat_completion) -> "LLMResponse":
        """Parse a Mistral ChatCompletion response into normalized form."""
        choice = chat_completion.choices[0]
        usage = chat_completion.usage
        return cls(
            content=choice.message.content,
            model=chat_completion.model,
            usage_prompt_tokens=usage.prompt_tokens,
            usage_completion_tokens=usage.completion_tokens,
            usage_total_tokens=usage.total_tokens,
            finish_reason=choice.finish_reason,
            raw_response=chat_completion,
        )


@dataclass
class StreamedChunk:
    """A single streamed chunk from a hosted LLM."""
    delta: str
    model: str
    finish_reason: Optional[str] = None

    @classmethod
    def from_mistral_chunk(cls, chunk) -> Optional["StreamedChunk"]:
        """Parse a Mistral streaming chunk."""
        choice = chunk.choices[0]
        delta = choice.delta.content or ""
        if delta or choice.finish_reason:
            return cls(
                delta=delta,
                model=chunk.model,
                finish_reason=choice.finish_reason,
            )
        return None


@dataclass
class SafetyResult:
    """Normalized safety / moderation result."""
    is_safe: bool = True
    categories: Dict[str, float] = field(default_factory=dict)
    flagged_categories: List[str] = field(default_factory=list)
    raw_response: Optional[Any] = None


@dataclass
class TranslationResult:
    """Normalized translation result."""
    translated_text: str
    source_language: str = "auto"
    target_language: str = "en"
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    """Normalized embedding result."""
    embeddings: List[List[float]]
    model: str = ""
    usage_prompt_tokens: int = 0
    raw_response: Optional[Any] = None


@dataclass
class SpeechResult:
    """Normalized text-to-speech result."""
    audio_url: Optional[str] = None
    audio_data: Optional[bytes] = None
    format: str = "mp3"
    raw_response: Optional[Any] = None


def normalize_model_name(family: str) -> str:
    """Map a model family name to a concrete Mistral model identifier."""
    family = family.lower().strip()
    if family in MISTRAL_MODEL_FAMILIES:
        return MISTRAL_MODEL_FAMILIES[family][0]
    return family


def build_json_extraction_prompt(text: str, schema: Optional[Dict] = None) -> str:
    """Build a prompt for JSON extraction from text."""
    base = (
        "Extract the key structured information from the following text and "
        "return it as valid JSON. Do not include markdown code fences or any "
        "text outside the JSON object.\n\n"
        f"Text:\n{text}\n\n"
        "JSON:"
    )
    if schema:
        base = (
            f"Extract structured information as JSON matching this schema:\n"
            f"{json.dumps(schema, indent=2)}\n\n"
            f"From the following text:\n{text}\n\n"
            "JSON:"
        )
    return base


def build_context_qa_prompt(context: str, question: str) -> str:
    """Build a prompt for answering questions with context."""
    return (
        "Use the following context to answer the question. If the context "
        "does not contain enough information, say so.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )


def build_summarization_prompt(text: str, max_length: int = 200) -> str:
    """Build a summarization prompt."""
    return (
        f"Summarize the following text in approximately {max_length} words or fewer. "
        "Focus on the main points and key takeaways.\n\n"
        f"Text:\n{text}\n\n"
        "Summary:"
    )
