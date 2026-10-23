from embeddings_client import embedding_model, get_client
from embeddings_models import normalize_vector


def embed_for_search(query: str, documents):
    items = [query] + list(documents)
    response = get_client().embeddings.create(model=embedding_model(), input=items)
    query_vector = normalize_vector(response.data[0].embedding)
    document_vectors = [normalize_vector(item.embedding) for item in response.data[1:]]
    return {"query": query_vector, "documents": document_vectors}


if __name__ == "__main__":
    print(embed_for_search("best cafes", ["coffee shop", "hardware store"]))
