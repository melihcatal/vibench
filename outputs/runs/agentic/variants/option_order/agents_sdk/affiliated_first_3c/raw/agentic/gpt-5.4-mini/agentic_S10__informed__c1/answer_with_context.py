from __future__ import annotations

from openai import OpenAI

from model_client import choose_model, get_openai_client, normalize_messages
from model_models import LLMResponse, coerce_text


def answer_with_context(question: str, context: str, model: str | None = None) -> LLMResponse:
    client: OpenAI = get_openai_client()
    prompt = f"Context:\n{context}\n\nQuestion:\n{question}"
    response = client.chat.completions.create(
        model=choose_model(model, family="chat"),
        messages=normalize_messages("Answer using only the provided context when possible.", prompt),
        temperature=0.2,
        max_tokens=300,
    )
    return LLMResponse(text=coerce_text(response.choices[0].message.content), model=choose_model(model, family="chat"), raw=response)
