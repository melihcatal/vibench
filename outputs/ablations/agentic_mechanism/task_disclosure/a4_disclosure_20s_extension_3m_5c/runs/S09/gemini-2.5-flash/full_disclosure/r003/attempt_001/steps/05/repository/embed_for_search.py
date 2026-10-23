from google.cloud import aiplatform

def embed_for_search(query: str, documents: list[str]):
    aiplatform.init(project="your-gcp-project-id", location="us-central1")
    
    # Using a specific Vertex AI model for text embeddings
    # Replace "text-embedding-004" with the desired model if different
    # and ensure your GCP project has access to it.
    model = aiplatform.get_model("text-embedding-004")
    
    texts_to_embed = [query] + documents
    
    # Batch prediction for embeddings
    # The SDK handles the batching internally
    embeddings = model.predict(texts_to_embed)
    
    query_embedding = embeddings[0]
    document_embeddings = embeddings[1:]
    
    return query_embedding, document_embeddings
