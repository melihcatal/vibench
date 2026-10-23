from google.cloud import aiplatform

def embed_for_search(project_id: str, location: str, query: str, documents: list[str]) -> dict:
    """Embeds a query and documents for semantic search using Vertex AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region for the Vertex AI endpoint (e.g., "us-central1").
        query: The search query string.
        documents: A list of document strings to embed.

    Returns:
        A dictionary containing 'query_embedding' and 'document_embeddings'.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

    all_texts = [query] + documents
    embeddings = model.get_embeddings(all_texts)

    query_embedding = embeddings[0].values
    document_embeddings = [emb.values for emb in embeddings[1:]]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }

if __name__ == '__main__':
    # Example usage:
    # project_id = "YOUR_PROJECT_ID"
    # location = "us-central1"
    # query = "What is machine learning?"
    # docs = [
    #     "Machine learning is a field of artificial intelligence.",
    #     "Deep learning is a subset of machine learning.",
    #     "Cloud computing provides scalable resources."
    # ]
    # search_embeddings = embed_for_search(project_id, location, query, docs)
    # print(f"Query embedding (first 5): {search_embeddings['query_embedding'][:5]}...")
    # print(f"Number of document embeddings: {len(search_embeddings['document_embeddings'])}")
    pass
