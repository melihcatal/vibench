from embeddings_client import get_embedding_client


def embed_for_search(query: str, documents):
    client, config = get_embedding_client()
    query_result = client.embeddings.create(model=config.model, input=query)
    doc_result = client.embeddings.create(model=config.model, input=list(documents))
    return {"query_embedding": query_result.data[0].embedding, "document_embeddings": [item.embedding for item in doc_result.data]}
