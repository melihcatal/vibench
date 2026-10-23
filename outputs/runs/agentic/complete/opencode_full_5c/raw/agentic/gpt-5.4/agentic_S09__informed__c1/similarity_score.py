from embeddings_client import DEFAULT_EMBED_MODEL, embed_single_text
from embeddings_models import cosine_similarity, ensure_single_text


def compute_similarity(
    text_a: str, text_b: str, *, model: str = DEFAULT_EMBED_MODEL
) -> float:
    left = embed_single_text(
        ensure_single_text(text_a), input_type="search_query", model=model
    )
    right = embed_single_text(
        ensure_single_text(text_b), input_type="search_query", model=model
    )
    return cosine_similarity(left.embedding, right.embedding)
