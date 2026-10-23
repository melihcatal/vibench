"""
Same-scenario: Answer a question using provided context with a hosted LLM.

Provider: OpenAI GPT via OpenAI API
SDK: openai
Auth: OPENAI_API_KEY
Model: gpt-4o
"""

from typing import Optional, List, Dict, Any

from model_client import create_openai_client, build_messages, get_default_model
from model_models import CompletionRequest, CompletionResponse


def answer_with_context(
    question: str,
    context: str,
    model: Optional[str] = None,
    max_answer_tokens: int = 1024,
    temperature: float = 0.3,
    system_prompt: Optional[str] = None,
    extra_context_items: Optional[List[str]] = None,
) -> CompletionResponse:
    """
    Answer a question using provided reference context via OpenAI GPT-4o.

    Args:
        question: The user's question to answer.
        context: The primary reference context text.
        model: The OpenAI model identifier. Defaults to gpt-4o.
        max_answer_tokens: Maximum tokens for the answer.
        temperature: Sampling temperature.
        system_prompt: Optional override for the system prompt.
        extra_context_items: Additional context strings to include.

    Returns:
        CompletionResponse containing the answer.
    """
    client = create_openai_client()

    default_system = (
        "You are a helpful assistant that answers questions based strictly "
        "on the provided context. If the answer cannot be determined from "
        "the context, say so clearly. Cite relevant parts of the context "
        "when possible."
    )

    system_prompt = system_prompt or default_system

    context_block = context
    if extra_context_items:
        for i, item in enumerate(extra_context_items, start=2):
            context_block += f"\n\n--- Additional Context {i} ---\n{item}"

    user_prompt = (
        f"Use the following context to answer the question.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}"
    )

    messages = build_messages(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    request = CompletionRequest(
        prompt=user_prompt,
        system_prompt=system_prompt,
        model=model or get_default_model(),
        temperature=temperature,
        max_tokens=max_answer_tokens,
    )

    response = client.chat.completions.create(
        **request.to_openai_kwargs(messages)
    )

    return CompletionResponse.from_openai_response(response)
