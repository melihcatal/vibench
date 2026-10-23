"""
Answer a question using provided context via OpenAI hosted LLM inference.
Provider: OpenAI Chat Completions API (model: gpt-4o)
SDK: openai
Auth: OPENAI_API_KEY
"""

from typing import Optional, Dict, Any
from model_client import get_client, DEFAULT_MODEL
from model_models import (
    LLMResponse,
    build_contextual_qa_request,
)


def answer_with_context(
    question: str,
    context: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 512,
) -> LLMResponse:
    """
    Answer a question using provided context via the OpenAI hosted LLM.

    Args:
        question: The question to answer.
        context: The reference context/document to use for answering.
        model: OpenAI model identifier (e.g., "gpt-4o", "gpt-4o-mini").
        temperature: Sampling temperature (lower = more focused on context).
        max_tokens: Maximum tokens for the answer.

    Returns:
        LLMResponse containing the answer and metadata.
    """
    request = build_contextual_qa_request(question, context)
    request.model = model
    request.temperature = temperature

    messages = request.to_messages()
    client = get_client()

    completion = client.create_chat_completion(
        messages=messages,
        model=request.model,
        temperature=request.temperature,
        max_tokens=max_tokens,
    )

    return LLMResponse.from_openai_completion(completion)


def answer_question_simple(
    question: str,
    context: str,
) -> str:
    """
    Simple function to get just the answer string.

    Args:
        question: The question to answer.
        context: The reference context.

    Returns:
        Answer string.
    """
    response = answer_with_context(question, context)
    return response.content


def batch_answer_with_context(
    qa_pairs: list[dict],
    shared_context: Optional[str] = None,
    model: str = DEFAULT_MODEL,
) -> list[dict]:
    """
    Answer multiple questions, optionally with shared context.

    Args:
        qa_pairs: List of dicts with "question" key and optional "context" key.
        shared_context: Optional context shared across all questions.
        model: OpenAI model identifier.

    Returns:
        List of dicts with question, answer, and metadata.
    """
    results = []
    for qa in qa_pairs:
        question = qa["question"]
        context = qa.get("context", "")
        if shared_context:
            context = f"{shared_context}\n\n{context}" if context else shared_context

        response = answer_with_context(question, context, model=model)
        results.append({
            "question": question,
            "answer": response.content,
            "model": response.model,
            "finish_reason": response.finish_reason,
        })
    return results


if __name__ == "__main__":
    import os
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY environment variable is required.")
    else:
        context_doc = (
            "The Python programming language was created by Guido van Rossum and was "
            "first released in 1991. Python emphasizes code readability with its notable "
            "use of significant whitespace. It supports multiple programming paradigms, "
            "including procedural, object-oriented, and functional programming. Python is "
            "dynamically typed and garbage-collected. It has a large standard library and "
            "a vast ecosystem of third-party packages available through PyPI."
        )
        question = "Who created Python and when was it first released?"
        result = answer_question_simple(question, context_doc)
        print(f"Question: {question}\nAnswer: {result}")
