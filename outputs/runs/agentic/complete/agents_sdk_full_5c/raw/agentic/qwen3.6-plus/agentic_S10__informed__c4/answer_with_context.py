"""
Answer a question using provided context with Anthropic Messages API and Claude.
Provider: Anthropic (anthropic SDK, ANTHROPIC_API_KEY)
"""

from typing import Optional, List, Dict, Any

import anthropic

from model_client import get_anthropic_client, normalize_completion_response
from model_models import LLMRequest, LLMResponse


DEFAULT_QA_MODEL = "claude-3-5-sonnet-20241022"


def answer_with_context(
    question: str,
    context: str,
    system_prompt: Optional[str] = None,
    model_id: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 2048,
) -> LLMResponse:
    """
    Answer a question using provided context via Anthropic Claude.

    Args:
        question: The question to answer.
        context: The context/knowledge base to use for answering.
        system_prompt: Optional custom system prompt.
        model_id: Anthropic model identifier.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens in the response.

    Returns:
        LLMResponse with the answer.
    """
    if model_id is None:
        model_id = DEFAULT_QA_MODEL

    if not system_prompt:
        system_prompt = (
            "You are a helpful answering assistant. Use only the provided context "
            "to answer the question. If the context does not contain enough "
            "information, say so clearly. Be concise and accurate."
        )

    user_prompt = (
        f"Context:\n---\n{context}\n---\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    request = LLMRequest(
        text=user_prompt,
        system_prompt=system_prompt,
        model_id=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    client = get_anthropic_client()

    api_request = request.to_anthropic_messages()
    response = client.messages.create(**api_request)

    normalized = normalize_completion_response(response)

    return LLMResponse(
        text=normalized["text"],
        model=normalized["model"],
        stop_reason=normalized["stop_reason"],
        input_tokens=normalized["usage"]["input_tokens"],
        output_tokens=normalized["usage"]["output_tokens"],
        raw_response=response,
    )


def answer_with_context_multi(
    question: str,
    contexts: List[str],
    model_id: str = DEFAULT_QA_MODEL,
) -> LLMResponse:
    """
    Answer using multiple context passages combined together.

    Args:
        question: The question to answer.
        contexts: List of context passages.
        model_id: Anthropic model identifier.

    Returns:
        LLMResponse with the answer.
    """
    combined = "\n\n".join(
        f"[Passage {i+1}]\n{ctx}" for i, ctx in enumerate(contexts)
    )
    return answer_with_context(question, combined, model_id=model_id)
