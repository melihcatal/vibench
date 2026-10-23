from __future__ import annotations

import os

from openai import OpenAI

from model_client import build_openai_client, resolve_reasoning_model
from model_models import normalize_text_response


SYSTEM_PROMPT = "Answer the question using only the provided context when possible."


def answer_with_context(question: str, context: str, *, client: OpenAI | None = None, model: str | None = None) -> str:
    api_client = client or build_openai_client()
    model_name = model or resolve_reasoning_model()
    response = api_client.responses.create(
        model=model_name,
        instructions=SYSTEM_PROMPT,
        input=f"Context:\n{context}\n\nQuestion:\n{question}",
    )
    return normalize_text_response(response)


if __name__ == "__main__":
    q = os.environ.get("QUESTION_TEXT", "")
    c = os.environ.get("CONTEXT_TEXT", "")
    if q and c:
        print(answer_with_context(q, c))
