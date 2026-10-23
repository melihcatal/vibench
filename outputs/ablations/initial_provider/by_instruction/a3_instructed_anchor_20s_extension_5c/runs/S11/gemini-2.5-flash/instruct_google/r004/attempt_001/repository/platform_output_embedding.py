from google.cloud import aiplatform

def platform_output_embedding(project_id: str, location: str, text_content: str):
    """Embeds Google Vertex AI platform outputs for evaluation or retrieval using Vertex AI Embedding API."""
    aiplatform.init(project=project_id, location=location)
    
    # Use the TextEmbeddingModel for generating embeddings
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko")
    
    embeddings = model.get_embeddings([text_content])
    
    # The embeddings object contains a list of Embedding objects. We extract the values.
    if embeddings:
        return {"text": text_content, "embedding": embeddings[0].values}
    return {"text": text_content, "embedding": []}
