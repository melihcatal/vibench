"""
model_models.py - Define local request, response, and normalization helpers
for Hosted LLM Inference and Model-Family Selection.

Uses OpenAI as the concrete hosted LLM provider.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LLMRequest:
    """Normalized request structure for LLM calls."""
    system_prompt: str
    user_content: str
    model_family: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    format_instructions: Optional[str] = None
    json_mode: bool = False

    def to_openai_params(self, model: str, messages: list[dict]) -> dict:
        """Convert to OpenAI API call parameters."""
        params = {
            "model": model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
        }
        if self.json_mode:
            params["response_format"] = {"type": "json_object"}
        return params


@dataclass
class LLMResponse:
    """Normalized response structure from LLM calls."""
    text: str = ""
    model_used: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    finish_reason: str = ""
    raw_response: Optional[Any] = field(default=None, repr=False)

    def to_dict(self) -> dict:
        """Convert response to dictionary."""
        return {
            "text": self.text,
            "model_used": self.model_used,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "finish_reason": self.finish_reason,
        }


@dataclass
class StreamChunk:
    """Normalized streaming chunk from LLM."""
    text_delta: str = ""
    is_last: bool = False
    model_used: str = ""
    raw_chunk: Optional[Any] = field(default=None, repr=False)


@dataclass
class SafetyCheckResult:
    """Result from a prompt safety check."""
    is_safe: bool = True
    categories: dict[str, bool] = field(default_factory=dict)
    flagged_categories: list[str] = field(default_factory=list)
    details: str = ""


@dataclass
class TranslationResult:
    """Result from translating model output."""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    model_used: str = ""


@dataclass
class EmbeddingResult:
    """Result from embedding model outputs."""
    embedding: list[float] = field(default_factory=list)
    model_used: str = ""
    dimensions: int = 0
    input_tokens: int = 0


def normalize_json_response(text: str) -> dict:
    """
    Parse and normalize a JSON string response from an LLM.
    Strips markdown code fences if present.
    """
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json"):].strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned[len("```"):].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM JSON response: {e}")


def normalize_stream_chunks(chunks: list[StreamChunk]) -> str:
    """Concatenate text deltas from streaming chunks into final text."""
    return "".join(chunk.text_delta for chunk in chunks if chunk.text_delta)


def build_summary_request(
    text: str,
    model_family: Optional[str] = None,
    max_words: int = 150,
) -> LLMRequest:
    """Build a standardized summarization request."""
    return LLMRequest(
        system_prompt=(
            "You are an expert summarizer. Provide concise, accurate summaries "
            "that capture the main points and key details."
        ),
        user_content=f"Summarize the following text in approximately {max_words} words:\n\n{text}",
        model_family=model_family,
        temperature=0.3,
        max_tokens=512,
    )


def build_extraction_request(
    text: str,
    schema_description: str,
    model_family: Optional[str] = None,
) -> LLMRequest:
    """Build a standardized JSON extraction request."""
    return LLMRequest(
        system_prompt=(
            "You are a data extraction expert. Extract structured information "
            "from text as valid JSON matching the requested schema."
        ),
        user_content=(
            f"Extract the following information from the text as JSON:\n"
            f"Schema: {schema_description}\n\n"
            f"Text:\n{text}"
        ),
        model_family=model_family,
        temperature=0.2,
        max_tokens=1024,
        json_mode=True,
        format_instructions="Return ONLY valid JSON. No explanations or markdown.",
    )


def build_context_qa_request(
    context: str,
    question: str,
    model_family: Optional[str] = None,
) -> LLMRequest:
    """Build a standardized context-based QA request."""
    return LLMRequest(
        system_prompt=(
            "You are a helpful assistant. Answer questions based only on the "
            "provided context. If the answer cannot be found in the context, "
            "say so explicitly."
        ),
        user_content=f"Context:\n{context}\n\nQuestion: {question}",
        model_family=model_family,
        temperature=0.3,
        max_tokens=512,
    )
