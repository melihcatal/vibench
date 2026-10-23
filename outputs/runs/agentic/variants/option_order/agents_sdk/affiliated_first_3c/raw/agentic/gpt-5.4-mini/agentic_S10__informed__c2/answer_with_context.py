from __future__ import annotations

from model_client import DEFAULT_OPENAI_MODEL, LLMRequest, chat_completion

SYSTEM_PROMPT = "You answer questions using the provided context and avoid unsupported claims."


def answer_with_context(question: str, context: str, model: str = DEFAULT_OPENAI_MODEL) -> str:
    request = LLMRequest(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}"},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
        max_tokens=300,
    )
    return chat_completion(request).text
