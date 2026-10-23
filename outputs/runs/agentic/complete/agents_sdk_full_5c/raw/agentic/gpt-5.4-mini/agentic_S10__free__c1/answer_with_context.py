from __future__ import annotations

from model_client import get_model_name, get_openai_client

PROVIDER = "openai"
MODEL_FAMILY = "gpt-4o"


def answer_with_context(question: str, context: str, model: str | None = None) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_model_name(model),
        input=[
            {
                "role": "system",
                "content": "Answer the question using only the provided context. If the context is insufficient, say so.",
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
        ],
    )
    return response.output_text
