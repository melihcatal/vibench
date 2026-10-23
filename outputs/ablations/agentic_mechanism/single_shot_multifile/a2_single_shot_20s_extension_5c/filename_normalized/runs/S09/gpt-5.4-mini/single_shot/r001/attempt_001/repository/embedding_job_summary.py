from collections.abc import Iterable
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_list


def embedding_job_summary(texts: Iterable[str], model: str | None = None) -> dict:
    client = get_embeddings_client()
    model_name = model or "text-embedding-3-small"
    batch = [str(text) for text in texts]
    response = client.embeddings.create(model=model_name, input=batch)
    embeddings = normalize_embedding_list(response)
    dims = len(embeddings[0]) if embeddings else 0
    return {
        "job_size": len(batch),
        "embedded_items": len(embeddings),
        "embedding_dimensions": dims,
        "model": model_name,
    }
