"""
Define local request, response, and normalization helpers for Hosted LLM Inference
and Model-Family Selection.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LLMRequest:
    """Normalized request payload for hosted LLM inference."""
    model: str
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: Optional[List[str]] = None
    response_format: Optional[Dict[str, Any]] = None
    stream: bool = False


@dataclass
class LLMResponse:
    """Normalized response payload from hosted LLM inference."""
    text: str
    model: str
    usage_prompt_tokens: int = 0
    usage_completion_tokens: int = 0
    usage_total_tokens: int = 0
    finish_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamChunk:
    """Normalized streaming chunk from hosted LLM."""
    text: str
    index: int
    finish_reason: Optional[str] = None
    model: Optional[str] = None


@dataclass
class EmbeddingResponse:
    """Normalized embedding response."""
    vectors: List[List[float]]
    model: str
    usage_tokens: int = 0


def normalize_openai_response(openai_response: Any) -> LLMResponse:
    """Convert an OpenAI API response to normalized LLMResponse."""
    choice = openai_response.choices[0]
    usage = openai_response.usage if openai_response.usage else {}
    return LLMResponse(
        text=choice.message.content if choice.message else "",
        model=openai_response.model,
        usage_prompt_tokens=getattr(usage, "prompt_tokens", 0),
        usage_completion_tokens=getattr(usage, "completion_tokens", 0),
        usage_total_tokens=getattr(usage, "total_tokens", 0),
        finish_reason=choice.finish_reason,
        metadata={
            "system_fingerprint": getattr(openai_response, "system_fingerprint", None),
            "created": getattr(openai_response, "created", None),
        },
    )


def normalize_openai_chunk(openai_chunk: Any) -> StreamChunk:
    """Convert an OpenAI streaming chunk to normalized StreamChunk."""
    delta = openai_chunk.choices[0].delta
    return StreamChunk(
        text=delta.content if delta and delta.content else "",
        index=openai_chunk.choices[0].index,
        finish_reason=openai_chunk.choices[0].finish_reason,
        model=openai_chunk.model,
    )


def build_system_prompt(task_type: str, **kwargs: Any) -> str:
    """Build a system prompt based on task type."""
    if task_type == "summarize":
        length = kwargs.get("length", "medium")
        return (
            f"You are a professional summarizer. "
            f"Produce a {length}-length summary that captures the key points, "
            f"main arguments, and essential conclusions. "
            f"Maintain factual accuracy and do not introduce new information."
        )
    elif task_type == "extract_json":
        schema_desc = kwargs.get("schema_description", "a valid JSON object")
        return (
            f"You are a structured data extraction assistant. "
            f"Extract information from the provided text and return ONLY valid JSON "
            f"matching the following schema: {schema_desc}. "
            f"Do not include markdown fences or explanations."
        )
    elif task_type == "answer_with_context":
        return (
            "You are a helpful question-answering assistant. "
            "Use ONLY the provided context to answer the question. "
            "If the answer cannot be found in the context, state that clearly. "
            "Do not make up information or use external knowledge."
        )
    elif task_type == "general":
        return "You are a helpful AI assistant."
    else:
        return kwargs.get("custom_system", "You are a helpful AI assistant.")


def build_completion_prompt(task_type: str, **kwargs: Any) -> str:
    """Build the user prompt based on task type."""
    if task_type == "summarize":
        text = kwargs.get("text", "")
        return f"Please summarize the following text:\n\n{text}"
    elif task_type == "extract_json":
        text = kwargs.get("text", "")
        return f"Extract structured JSON from the following text:\n\n{text}"
    elif task_type == "answer_with_context":
        context = kwargs.get("context", "")
        question = kwargs.get("question", "")
        return f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    elif task_type == "stream":
        prompt = kwargs.get("prompt", "")
        return prompt
    else:
        return kwargs.get("user_message", "")


MODEL_FAMILIES = {
    "openai": {
        "gpt-4o": "openai/gpt-4o",
        "gpt-4o-mini": "openai/gpt-4o-mini",
        "gpt-4-turbo": "openai/gpt-4-turbo",
        "gpt-3.5-turbo": "openai/gpt-3.5-turbo",
    },
    "anthropic": {
        "claude-3-opus": "anthropic/claude-3-opus-20240229",
        "claude-3-sonnet": "anthropic/claude-3-sonnet-20240229",
        "claude-3-haiku": "anthropic/claude-3-haiku-20240307",
    },
}


def resolve_model_identifier(model_family: str, model_name: str) -> str:
    """Resolve a model family and name to a concrete model identifier."""
    family_map = MODEL_FAMILIES.get(model_family, {})
    return family_map.get(model_name, f"{model_family}/{model_name}")
