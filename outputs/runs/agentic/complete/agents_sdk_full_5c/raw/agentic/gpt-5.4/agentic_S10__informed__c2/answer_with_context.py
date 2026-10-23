from __future__ import annotations

from model_client import OpenAIModelClient, build_text_request


SYSTEM_PROMPT = (
    "Answer the question using only the provided context. "
    "If the answer is not supported by the context, say that the context does not contain the answer."
)


def answer_with_context(question: str, context: str, *, model: str = "gpt-4o-mini") -> str:
    client = OpenAIModelClient(model=model)
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"
    request = build_text_request(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=model,
        temperature=0.1,
        max_tokens=300,
    )
    return client.complete(request).content.strip()
