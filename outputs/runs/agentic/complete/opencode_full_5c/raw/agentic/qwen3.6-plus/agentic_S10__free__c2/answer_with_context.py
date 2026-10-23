from __future__ import annotations

from typing import Optional

from model_client import call_llm
from model_models import LLMRequest, LLMResponse, normalize_prompt

CONTEXT_ANSWER_MODEL = "gpt-4o"
CONTEXT_ANSWER_SYSTEM_PROMPT = (
    "You are a precise question-answering assistant. Answer the user's question using ONLY "
    "the provided context. If the context does not contain sufficient information to answer, "
    "state that clearly. Do not fabricate or hallucinate information."
)


def answer_with_context(
    question: str,
    context: str,
    temperature: float = 0.2,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    normalized_context = normalize_prompt(context)
    prompt = (
        f"Context:\n{normalized_context}\n\n"
        f"Question: {question}\n\n"
        f"Answer based only on the context above:"
    )
    request = LLMRequest(
        model=model or CONTEXT_ANSWER_MODEL,
        prompt=prompt,
        system_prompt=CONTEXT_ANSWER_SYSTEM_PROMPT,
        temperature=temperature,
        max_tokens=1024,
    )
    return call_llm(request, api_key=api_key, base_url=base_url)


def answer_with_citations(
    question: str,
    context: str,
    temperature: float = 0.2,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> LLMResponse:
    normalized_context = normalize_prompt(context)
    prompt = (
        f"Context:\n{normalized_context}\n\n"
        f"Question: {question}\n\n"
        f"Answer the question using the context. Include direct quotes from the context "
        f"to support your answer, citing the relevant passage."
    )
    request = LLMRequest(
        model=model or CONTEXT_ANSWER_MODEL,
        prompt=prompt,
        system_prompt=CONTEXT_ANSWER_SYSTEM_PROMPT,
        temperature=temperature,
        max_tokens=2048,
    )
    return call_llm(request, api_key=api_key, base_url=base_url)


if __name__ == "__main__":
    import os

    response = answer_with_context(
        question="What is the capital of France?",
        context="France is a country in Western Europe. Its capital and largest city is Paris...",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    print(response.text)
