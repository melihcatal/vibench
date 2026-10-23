import os
import vertexai
from typing import List
from safety_client import SafetyClient
from vertexai.language_models import TextEmbeddingModel

def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationales for case retrieval using Google Cloud Vertex AI's embedding model.
    """
    safety_client = SafetyClient()
    # For embeddings, we use the specific TextEmbeddingModel
    # The model ID for text embeddings is typically 'text-embedding-004' or similar.
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = []
    # The embedding model can take a batch of texts
    if reasons:
        response = model.predict(reasons)
        for embedding in response.embeddings:
            embeddings.append(embedding.values)

    return embeddings
