from __future__ import annotations

from embeddings_client import get_embeddings_client, resolve_embedding_model
from embeddings_models import cosine_similarity, normalize_text, parse_embedding_response


def similarity_score(text_a: str, text_b: str, model: str | None = None) -> float:
    client = get_embeddings_client()
    selected_model = resolve_embedding_model(model)
    response = client.embeddings.create(
        model=selected_model,
        input=[normalize_text(text_a), normalize_text(text_b)],
    )
    parsed = parse_embedding_response(response)
    return cosine_similarity(parsed.data[0].embedding, parsed.data[1].embedding)
