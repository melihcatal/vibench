from __future__ import annotations

from model_client import DEFAULT_CHAT_MODEL, build_chat_request, get_openai_client
from model_models import normalize_generation_response


def answer_with_context(question: str, context: str) -> dict:
    client = get_openai_client()
    prompt = f"Context:\n{context}\n\nQuestion:\n{question}"
    request = build_chat_request(
        "Answer the question using only the supplied context. If unsupported, say so clearly.",
        prompt,
        model=DEFAULT_CHAT_MODEL,
        temperature=0.1,
        max_output_tokens=300,
    )
    response = client.chat.completions.create(**request.to_openai())
    result = normalize_generation_response(response)
    return {"answer": result.text, "model": result.model, "usage": result.usage}
