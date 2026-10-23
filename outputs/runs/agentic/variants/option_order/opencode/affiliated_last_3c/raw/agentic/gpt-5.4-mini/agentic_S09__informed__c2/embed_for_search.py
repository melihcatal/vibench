from embeddings_client import create_client, get_model_name


def embed_for_search(query: str, documents):
    client = create_client()
    model = get_model_name()
    items = [query] + list(documents)
    response = client.embeddings.create(model=model, input=items)
    return {
        "query_embedding": response.data[0].embedding,
        "document_embeddings": [item.embedding for item in response.data[1:]],
    }
