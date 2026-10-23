from embeddings_client import get_bedrock_client


def embed_for_search(query, documents, config=None):
    client = get_bedrock_client(config)
    query_embedding = embed_text({"text": query}, config=config)
    document_embeddings = embed_batch([{"text": doc} for doc in documents], config=config)
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}