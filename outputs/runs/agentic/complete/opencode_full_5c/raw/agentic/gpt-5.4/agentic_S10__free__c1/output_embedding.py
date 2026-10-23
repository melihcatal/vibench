from __future__ import annotations

from model_client import choose_model, get_client


def output_embedding(text: str, model: str | None = None) -> dict:
    selected_model = choose_model("embed", model)
    response = get_client().embeddings.create(model=selected_model, input=text)
    item = response.data[0]
    return {
        "provider": "openai",
        "model": selected_model,
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
    }
