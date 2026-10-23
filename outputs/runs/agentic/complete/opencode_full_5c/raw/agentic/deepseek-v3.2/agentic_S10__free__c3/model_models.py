from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class SummaryRequest:
    """Request for text summarization."""

    text: str
    max_length: Optional[int] = None
    model: Optional[str] = None


@dataclass
class SummaryResponse:
    """Response from text summarization."""

    original_text: str
    summary: str
    model_used: str
    provider: str
    timestamp: datetime = datetime.now()


@dataclass
class JsonExtractionRequest:
    """Request for JSON extraction."""

    text: str
    schema: Optional[Dict[str, Any]] = None
    model: Optional[str] = None


@dataclass
class JsonExtractionResponse:
    """Response from JSON extraction."""

    original_text: str
    extracted_json: Dict[str, Any]
    model_used: str
    provider: str
    timestamp: datetime = datetime.now()


@dataclass
class ContextAnswerRequest:
    """Request for context-based answering."""

    question: str
    context: str
    model: Optional[str] = None


@dataclass
class ContextAnswerResponse:
    """Response from context-based answering."""

    question: str
    context: str
    answer: str
    model_used: str
    provider: str
    timestamp: datetime = datetime.now()


@dataclass
class StreamCompletionRequest:
    """Request for streaming completion."""

    prompt: str
    model: Optional[str] = None
    max_tokens: int = 500


@dataclass
class StreamChunk:
    """Chunk from streaming completion."""

    chunk_text: str
    full_text_so_far: str
    model_used: str
    provider: str
    timestamp: datetime = datetime.now()


@dataclass
class ModelUsage:
    """Usage statistics for model calls."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: Optional[float] = None


@dataclass
class ModelSelection:
    """Model selection criteria."""

    task_type: str
    required_capabilities: List[str]
    budget_constraint: Optional[float] = None
    latency_requirement: Optional[float] = None


def normalize_model_response(response: Any, provider: str) -> Dict[str, Any]:
    """
    Normalize model response from different providers.

    Args:
        response: Raw response from provider
        provider: Provider name

    Returns:
        Normalized response dictionary
    """
    if provider == "openai":
        if hasattr(response, "choices") and len(response.choices) > 0:
            return {
                "text": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens
                    if hasattr(response.usage, "prompt_tokens")
                    else 0,
                    "completion_tokens": response.usage.completion_tokens
                    if hasattr(response.usage, "completion_tokens")
                    else 0,
                    "total_tokens": response.usage.total_tokens
                    if hasattr(response.usage, "total_tokens")
                    else 0,
                },
            }
    elif provider == "anthropic":
        if hasattr(response, "content"):
            return {
                "text": response.content[0].text
                if hasattr(response.content[0], "text")
                else str(response.content),
                "model": response.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens
                    if hasattr(response.usage, "input_tokens")
                    else 0,
                    "output_tokens": response.usage.output_tokens
                    if hasattr(response.usage, "output_tokens")
                    else 0,
                },
            }

    return {"text": str(response), "model": "unknown", "usage": {}}


def estimate_cost(usage: Dict[str, int], model: str, provider: str) -> float:
    """
    Estimate cost based on usage and model.

    Args:
        usage: Token usage dictionary
        model: Model name
        provider: Provider name

    Returns:
        Estimated cost in USD
    """
    if provider == "openai":
        if "gpt-4o" in model:
            input_cost = 2.50 / 1_000_000  # $2.50 per 1M input tokens
            output_cost = 10.00 / 1_000_000  # $10.00 per 1M output tokens
        elif "gpt-4o-mini" in model:
            input_cost = 0.15 / 1_000_000  # $0.15 per 1M input tokens
            output_cost = 0.60 / 1_000_000  # $0.60 per 1M output tokens
        else:
            input_cost = 0.50 / 1_000_000  # Default
            output_cost = 1.50 / 1_000_000  # Default

        prompt_tokens = usage.get("prompt_tokens", usage.get("input_tokens", 0))
        completion_tokens = usage.get(
            "completion_tokens", usage.get("output_tokens", 0)
        )

        return (prompt_tokens * input_cost) + (completion_tokens * output_cost)

    elif provider == "anthropic":
        if "claude-3-5-sonnet" in model:
            input_cost = 3.00 / 1_000_000  # $3.00 per 1M input tokens
            output_cost = 15.00 / 1_000_000  # $15.00 per 1M output tokens
        elif "claude-3-opus" in model:
            input_cost = 15.00 / 1_000_000  # $15.00 per 1M input tokens
            output_cost = 75.00 / 1_000_000  # $75.00 per 1M output tokens
        else:
            input_cost = 0.80 / 1_000_000  # Default
            output_cost = 4.00 / 1_000_000  # Default

        input_tokens = usage.get("input_tokens", usage.get("prompt_tokens", 0))
        output_tokens = usage.get("output_tokens", usage.get("completion_tokens", 0))

        return (input_tokens * input_cost) + (output_tokens * output_cost)

    return 0.0
