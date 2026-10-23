"""
Call a hosted LLM (OpenAI gpt-4o) to answer a question using provided context.

Uses OpenAI platform API at api.openai.com with concrete model gpt-4o
for retrieval-augmented generation (RAG) style Q&A.
"""

from typing import Any, Dict, List, Optional

from model_client import create_openai_client, execute_chat_completion
from model_models import LLMRequest, build_system_prompt, build_completion_prompt


def answer_with_context(
    question: str,
    context: str,
    model: str = "gpt-4o",
    temperature: float = 0.3,
    max_tokens: int = 512,
) -> str:
    """Answer a question using only the provided context via OpenAI's hosted LLM.

    Args:
        question: The question to answer.
        context: The reference context/document content.
        model: OpenAI model identifier (defaults to gpt-4o).
        temperature: Sampling temperature (lower for factual answers).
        max_tokens: Maximum tokens in the output.

    Returns:
        The answer text string.
    """
    system_prompt = build_system_prompt("answer_with_context")
    user_prompt = build_completion_prompt(
        "answer_with_context", context=context, question=question
    )

    request = LLMRequest(
        model=model,
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    response = execute_chat_completion(request)
    return response.text


def answer_multi_context(
    question: str,
    contexts: List[str],
    model: str = "gpt-4o",
    temperature: float = 0.3,
) -> str:
    """Answer a question using multiple context passages via OpenAI gpt-4o.

    Args:
        question: The question to answer.
        contexts: List of context passages/documents.
        model: OpenAI model identifier.
        temperature: Sampling temperature.

    Returns:
        The synthesized answer text.
    """
    combined_context = "\n\n---\n\n".join(
        f"[Passage {i+1}]:\n{ctx}" for i, ctx in enumerate(contexts)
    )

    system_prompt = (
        "You are a research assistant. Answer the question using ONLY the provided "
        "passages. If multiple passages contain relevant information, synthesize them. "
        "If the answer cannot be determined from the passages, say so explicitly."
    )

    request = LLMRequest(
        model=model,
        prompt=f"Context:\n{combined_context}\n\nQuestion: {question}\n\nAnswer:",
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=768,
    )

    response = execute_chat_completion(request)
    return response.text


def answer_with_citations(
    question: str,
    context: str,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """Answer with inline citations to the context using OpenAI gpt-4o.

    Args:
        question: The question to answer.
        context: The reference context.
        model: OpenAI model identifier.

    Returns:
        Dict with 'answer' text and 'citations' list of quoted context spans.
    """
    system_prompt = (
        "Answer the question using the provided context. Include inline citations "
        "by quoting the relevant passage from the context. Return your response as "
        "a JSON object with 'answer' and 'citations' fields. The citations field "
        "should be a list of exact quotes from the context that support your answer."
    )

    request = LLMRequest(
        model=model,
        prompt=f"Context:\n{context}\n\nQuestion: {question}",
        system_prompt=system_prompt,
        temperature=0.2,
        max_tokens=1024,
        response_format={"type": "json_object"},
    )

    response = execute_chat_completion(request)
    import json

    result_text = response.text.strip()
    if result_text.startswith("```"):
        lines = result_text.split("\n")
        lines = lines[1:] if lines[0].startswith("```") else lines
        lines = lines[:-1] if lines and lines[-1].strip().startswith("```") else lines
        result_text = "\n".join(lines).strip()

    return json.loads(result_text)


if __name__ == "__main__":
    ctx = (
        "The Python programming language was created by Guido van Rossum and first "
        "released in 1991. It emphasizes code readability with its use of significant "
        "whitespace. Python supports multiple paradigms including procedural, "
        "object-oriented, and functional programming."
    )
    q = "Who created Python and when was it released?"
    answer = answer_with_context(q, ctx)
    print(answer)
