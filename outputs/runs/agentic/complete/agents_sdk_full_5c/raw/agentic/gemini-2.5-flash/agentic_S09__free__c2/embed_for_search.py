from google.cloud import aiplatform

def embed_for_search(project_id: str, location: str, query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """Embeds a query and multiple documents for semantic search using Vertex AI.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region for the Vertex AI endpoint (e.g., "us-central1").
        query: The search query string.
        documents: A list of document strings to embed.

    Returns:
        A tuple containing:
            - The embedding vector for the query.
            - A list of embedding vectors for the documents.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

    all_texts = [query] + documents
    embeddings = model.get_embeddings(all_texts)

    query_embedding = embeddings[0].values
    document_embeddings = [emb.values for emb in embeddings[1:]]

    return query_embedding, document_embeddings

if __name__ == '__main__':
    # This is a placeholder for actual usage.
    # Replace with your project_id and desired location.
    # query_vec, doc_vecs = embed_for_search(
    #     project_id="your-project-id", 
    #     location="us-central1", 
    #     query="What is machine learning?", 
    #     documents=["Machine learning is a field of artificial intelligence.", "Deep learning is a subset of machine learning."]
    # )
    # print(f"Query embedding length: {len(query_vec)}")
    # print(f"Number of document embeddings: {len(doc_vecs)}")
    pass
