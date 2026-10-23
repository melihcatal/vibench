from __future__ import annotations

from model_client import get_openai_client, select_model


def embed_output(texts: list[str], model: str | None = None) -> dict:
    client = get_openai_client()
    embedding_model = select_model("embedding", model)
    response = client.embeddings.create(
        model=embedding_model,
        input=texts,
    )
    vectors = [item.embedding for item in response.data]
    usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else {}
    return {"model": embedding_model, "embeddings": vectors, "usage": usage}
