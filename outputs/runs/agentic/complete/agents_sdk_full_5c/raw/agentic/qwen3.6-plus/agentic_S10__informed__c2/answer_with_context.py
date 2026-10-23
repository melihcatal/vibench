"""
Answer a question using provided context with a hosted LLM.

Provider: OpenAI Chat Completions API
SDK: openai
Auth: OPENAI_API_KEY
Concrete model: gpt-4o
Endpoint: api.openai.com/v1/chat/completions
"""

from typing import Optional

from model_client import call_llm_sync
from model_models import (
    LLMRequest,
    LLMResponse,
    build_context_qa_request,
)


def answer_with_context(
    context: str,
    question: str,
    model_name: Optional[str] = None,
) -> LLMResponse:
    """
    Answer a question using the provided context via OpenAI gpt-4o.

    Args:
        context: The reference context document or passage.
        question: The question to answer.
        model_name: Optional model override (default: gpt-4o).

    Returns:
        LLMResponse containing the model's answer.
    """
    effective_model = model_name or "gpt-4o"
    request = build_context_qa_request(
        context=context,
        question=question,
        model_name=effective_model,
    )
    return call_llm_sync(request)


def answer_with_context_custom(
    context: str,
    question: str,
    system_prompt: str,
    model_name: str = "gpt-4o",
    temperature: float = 0.3,
) -> LLMResponse:
    """
    Answer a question with custom system prompt via OpenAI.

    Args:
        context: The reference context.
        question: The question to answer.
        system_prompt: Custom system prompt.
        model_name: OpenAI model identifier (e.g., gpt-4o, gpt-4o-mini).
        temperature: Sampling temperature.

    Returns:
        LLMResponse containing the answer.
    """
    user_content = f"Context:\n{context}\n\nQuestion: {question}"
    request = LLMRequest(
        user_prompt=user_content,
        system_prompt=system_prompt,
        model_name=model_name,
        temperature=temperature,
        max_tokens=1024,
    )
    return call_llm_sync(request)
