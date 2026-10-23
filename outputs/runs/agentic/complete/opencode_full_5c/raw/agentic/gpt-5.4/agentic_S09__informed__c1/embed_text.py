from embeddings_client import DEFAULT_EMBED_MODEL, embed_single_text
from embeddings_models import ensure_single_text


def generate_embedding(text: str, *, model: str = DEFAULT_EMBED_MODEL) -> list[float]:
    normalized_text = ensure_single_text(text)
    result = embed_single_text(
        normalized_text, input_type="search_document", model=model
    )
    return result.embedding
