"""
Answer a question using provided context via a hosted LLM.
Provider: OpenAI - https://platform.openai.com
Model: gpt-4o (openai-gpt4o family)
"""

from typing import Optional, List
from model_client import get_openai_client, resolve_model_family, DEFAULT_QA_MODEL
from model_models import (
    LLMRequest,
    LLMResponse,
    normalize_messages_with_context,
)


QA_SYSTEM_PROMPT = (
    "You are a helpful question-answering assistant. Answer the user's question "
    "using ONLY the provided context. If the answer cannot be determined from "
    "the context, state that clearly. Do not use outside knowledge. Be concise "
    "and cite specific details from the context when possible."
)


def answer_with_context(
    context: str,
    question: str,
    model: str = DEFAULT_QA_MODEL,
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    """
    Send a question and context to the OpenAI gpt-4o model at api.openai.com
    and return a grounded answer.

    Args:
        context: The reference text to ground the answer in.
        question: The question to answer.
        model: OpenAI model identifier (default: gpt-4o).
        temperature: Sampling temperature.
        max_tokens: Maximum output tokens.
        api_key: Optional override for OPENAI_API_KEY.
        base_url: Optional override for OpenAI API endpoint.

    Returns:
        LLMResponse containing the answer text and metadata.
    """
    messages = normalize_messages_with_context(
        system_prompt=QA_SYSTEM_PROMPT,
        context=context,
        question=question,
    )

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    client = get_openai_client(api_key=api_key, base_url=base_url)
    openai_kwargs = request.to_openai_kwargs()
    response = client.chat.completions.create(**openai_kwargs)

    return LLMResponse.from_openai(response, model=model)


def answer_multi_turn_with_context(
    context: str,
    conversation: List[dict],
    model: str = DEFAULT_QA_MODEL,
    temperature: float = 0.2,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    """
    Answer questions in a multi-turn conversation grounded in context,
    using the OpenAI gpt-4o model.

    Args:
        context: The reference document or passage.
        conversation: List of message dicts with 'role' and 'content'.
        model: OpenAI model identifier.
        temperature: Sampling temperature.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        LLMResponse with the assistant's reply.
    """
    messages = [
        {"role": "system", "content": QA_SYSTEM_PROMPT + f"\n\nContext:\n{context}"}
    ]
    messages.extend(conversation)

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
    )

    client = get_openai_client(api_key=api_key, base_url=base_url)
    openai_kwargs = request.to_openai_kwargs()
    response = client.chat.completions.create(**openai_kwargs)

    return LLMResponse.from_openai(response, model=model)


if __name__ == "__main__":
    ctx = (
        "The Eiffel Tower was completed in 1889 for the World's Fair in Paris. "
        "It stands 330 meters tall and was designed by Gustave Eiffel's engineering company. "
        "Initially criticized by artists, it has become one of the most visited paid monuments "
        "in the world, attracting nearly 7 million visitors annually."
    )
    q = "When was the Eiffel Tower completed and how tall is it?"
    result = answer_with_context(context=ctx, question=q)
    print(f"Model family: {resolve_model_family(result.model)}")
    print(f"Answer: {result.text}")
