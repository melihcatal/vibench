from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import build_client, model_for_task
from model_models import ChatRequest, normalize_text


OPENAI_QA_MODEL = "gpt-4o"


def answer_with_context(question: str, context: str, client: Optional[OpenAI] = None) -> str:
    client = client or build_client()
    request = ChatRequest(
        task="answer_with_context",
        model=model_for_task("answer_with_context", default=OPENAI_QA_MODEL),
        system_prompt="You answer questions using only the provided context when possible.",
        user_prompt=f"Context:\n{context}\n\nQuestion:\n{question}",
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=request.messages(),
        temperature=0.1,
    )
    return normalize_text(response.choices[0].message.content or "")
