from embeddings_client import DEFAULT_EMBED_MODEL, embed_texts
from embeddings_models import normalize_texts


def generate_batch_embeddings(
    texts: list[str], *, model: str = DEFAULT_EMBED_MODEL
) -> list[list[float]]:
    normalized = normalize_texts(texts)
    if not normalized:
        return []
    results = embed_texts(normalized, input_type="search_document", model=model)
    return [item.embedding for item in results]
