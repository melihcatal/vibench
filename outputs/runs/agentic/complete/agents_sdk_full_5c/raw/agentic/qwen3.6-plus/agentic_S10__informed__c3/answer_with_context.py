"""
Answer a question using provided context with a Mistral AI hosted LLM.

Provider: Mistral AI Chat API
SDK: mistralai
Auth: MISTRAL_API_KEY
"""

from __future__ import annotations

from typing import Optional

from model_client import build_request, create_mistral_client, execute_chat
from model_models import (
    LLMResponse,
    LLMRequest,
    build_context_qa_prompt,
)


def answer_with_context(
    context: str,
    question: str,
    model: Optional[str] = None,
    temperature: float = 0.3,
) -> LLMResponse:
    """Answer a question using the provided context via a Mistral AI model.

    Args:
        context: The reference context / knowledge to use.
        question: The question to answer.
        model: Optional concrete Mistral model identifier (e.g., 'mistral-large-latest').
        temperature: Sampling temperature.

    Returns:
        LLMResponse containing the answer.
    """
    prompt = build_context_qa_prompt(context, question)

    system_prompt = (
        "You are a helpful assistant that answers questions based on the provided "
        "context. If the context does not contain enough information to answer, "
        "clearly state that. Be precise and factual."
    )

    request = build_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=1024,
        temperature=temperature,
    )

    return execute_chat(request)


def answer_with_context_with_client(
    context: str,
    question: str,
    client,
    model: Optional[str] = None,
    temperature: float = 0.3,
) -> LLMResponse:
    """Answer a question using a pre-created Mistral client.

    Args:
        context: The reference context / knowledge to use.
        question: The question to answer.
        client: An initialized mistralai.Mistral client.
        model: Optional concrete Mistral model identifier.
        temperature: Sampling temperature.

    Returns:
        LLMResponse containing the answer.
    """
    prompt = build_context_qa_prompt(context, question)

    system_prompt = (
        "You are a helpful assistant that answers questions based on the provided "
        "context. If the context does not contain enough information to answer, "
        "clearly state that. Be precise and factual."
    )

    request = build_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        max_tokens=1024,
        temperature=temperature,
    )

    return execute_chat(request, client=client)
