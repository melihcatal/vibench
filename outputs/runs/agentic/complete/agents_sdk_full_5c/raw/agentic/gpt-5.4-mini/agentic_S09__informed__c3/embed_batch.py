from embeddings_client import get_client, get_model, normalize_text, resolve_input_type
from embeddings_models import normalize_embedding


def embed_batch(texts: list[str]) -> list[list[float]]:
    client = get_client()
    response = client.embed(
        texts=[normalize_text(text) for text in texts],
        model=get_model(),
        input_type=resolve_input_type("search_document"),
        embedding_types=["float"],
    )
    return [normalize_embedding(item) for item in response.embeddings.float]
