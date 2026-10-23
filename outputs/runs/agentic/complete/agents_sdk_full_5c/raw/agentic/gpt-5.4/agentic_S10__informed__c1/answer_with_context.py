from __future__ import annotations

from model_client import HostedModelClient
from model_models import GenerationOptions, build_messages


def answer_with_context(question: str, context: str) -> str:
    client = HostedModelClient()
    model = client.select_model_family("answer")
    prompt = (
        "Use only the provided context to answer the question. "
        "If the answer is not supported by the context, say that the context does not contain the answer.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    messages = build_messages(
        system_prompt="You are a grounded question answering assistant.",
        user_prompt=prompt,
    )
    result = client.chat(
        messages,
        GenerationOptions(model=model, temperature=0.1, max_tokens=220),
    )
    return result.text
