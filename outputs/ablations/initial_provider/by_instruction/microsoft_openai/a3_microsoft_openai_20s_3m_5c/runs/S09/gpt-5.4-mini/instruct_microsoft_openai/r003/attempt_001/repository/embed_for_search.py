from embeddings_client import embedding_model, get_client
from embeddings_models import normalize_vectors


def embed_for_search(query: str, documents: list[str]) -> dict[str, list]:
    client = get_client()
    response = client.embeddings.create(model=embedding_model(), input=[query] + documents)
    vectors = normalize_vectors([item.embedding for item in response.data])
    return {"query": vectors[0], "documents": vectors[1:]}
