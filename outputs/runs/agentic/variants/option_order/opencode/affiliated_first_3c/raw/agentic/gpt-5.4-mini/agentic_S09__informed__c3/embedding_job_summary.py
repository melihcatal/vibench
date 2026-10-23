from embeddings_client import get_embeddings_client, default_embedding_model
from embeddings_models import coerce_embeddings


def embedding_job_summary(texts, model: str | None = None):
    client = get_embeddings_client()
    response = client.embeddings.create(model=model or default_embedding_model(), input=list(texts))
    vectors = coerce_embeddings(response)
    dimensions = len(vectors[0]) if vectors else 0
    return {"provider": "openai", "count": len(vectors), "dimensions": dimensions}
