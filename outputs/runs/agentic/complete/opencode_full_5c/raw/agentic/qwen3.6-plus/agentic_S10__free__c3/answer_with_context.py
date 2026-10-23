from __future__ import annotations

from typing import Dict, List, Optional

from model_client import create_completion
from model_models import LLMRequest, normalize_messages


def answer_with_context(
    question: str,
    context: str,
    system_prompt: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
    model: str = "gpt-4o-2024-08-06",
    temperature: float = 0.5,
) -> str:
    default_system = (
        "You are a helpful assistant that answers questions based strictly on the provided context. "
        "If the answer cannot be determined from the context, say so clearly."
    )
    system = system_prompt or default_system

    messages = normalize_messages(
        system_prompt=system,
        user_prompt=question,
        context=context,
        history=history,
    )

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=1024,
    )
    response = create_completion(request)
    return response.content


if __name__ == "__main__":
    import sys

    context_input = sys.stdin.read()
    question = "What are the key points?"
    result = answer_with_context(question=question, context=context_input)
    print(result)
