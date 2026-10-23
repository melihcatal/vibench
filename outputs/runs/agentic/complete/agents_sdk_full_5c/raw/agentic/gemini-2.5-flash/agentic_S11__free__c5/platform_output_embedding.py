import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_platform_outputs(project_id: str, location: str, texts: list[str]) -> list[list[float]]:
    """Embeds platform outputs using Google Cloud Vertex AI Text Embedding."""
    vertexai.init(project=project_id, location=location)
    
    # The embedding model to use.
    # For text-embedding-004, the maximum number of texts per request is 5.
    # For text-embedding-gecko@001 and earlier, it's 100.
    # Adjust batching logic if `texts` can be large.
    model = TextEmbeddingModel.from_pretrained("text-embedding-004") 
    
    embeddings = model.get_embeddings(texts)
    
    return [embedding.values for embedding in embeddings]
