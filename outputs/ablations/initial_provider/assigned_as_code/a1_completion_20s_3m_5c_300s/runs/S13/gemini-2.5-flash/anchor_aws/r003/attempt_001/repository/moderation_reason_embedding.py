import os
from typing import List
from google.cloud import aiplatform

def embed_moderation_rationales(texts: List[str], project_id: str, location: str = "us-central1") -> List[List[float]]:
    """Embed moderation rationales for case retrieval using Google Cloud Vertex AI's embedding model."""
    
    aiplatform.init(project=project_id, location=location)
    
    # Use the text-embedding-004 model for embeddings
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("text-embedding-004")

    # The predict method can take a list of texts
    embeddings = model.predict(texts)
    
    return [embedding.values for embedding in embeddings]
