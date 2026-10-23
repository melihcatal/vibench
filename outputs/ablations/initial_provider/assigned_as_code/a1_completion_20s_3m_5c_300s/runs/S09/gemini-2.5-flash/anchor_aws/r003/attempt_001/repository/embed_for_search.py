from embeddings_client import BedrockEmbeddingsClient

def embed_for_search(payload, config=None):
    config = config or {}
    client = BedrockEmbeddingsClient(
        region_name=config.get("region"),
        model_id="amazon.titan-embed-text-v2:0"
    )

    query_text = payload["query"]
    document_texts = payload["documents"]

    query_embedding_response = client.invoke_model(query_text)
    query_embedding = query_embedding_response["embedding"]

    document_embeddings = []
    for doc_text in document_texts:
        doc_embedding_response = client.invoke_model(doc_text)
        document_embeddings.append(doc_embedding_response["embedding"])

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings
    }
