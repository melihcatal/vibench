from google.cloud import aiplatform

def embed_document_sections(project_id: str, location: str, texts: list[str]) -> list[list[float]]:
    """Embeds extracted document sections for semantic retrieval using Google Cloud Vertex AI Text Embedding Model."""
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.predict(texts)
    
    # The predict method returns a list of TextEmbedding objects, each containing a list of floats
    # We want to return a list of lists of floats.
    return [embedding.values for embedding in embeddings]
