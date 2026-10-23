from typing import List
import os

from google.cloud import aiplatform

def embed_audit_notes(audit_notes: List[str]) -> List[List[float]]:
    """
    Embeds crypto audit notes using Google Cloud Vertex AI's TextEmbeddingModel.

    Args:
        audit_notes: A list of strings, where each string is a crypto audit note.

    Returns:
        A list of lists of floats, where each inner list is the embedding for a corresponding audit note.
    """
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION"))
    
    # Using the text-embedding-004 model for text embeddings
    # This model is identifiable as a Google Cloud Vertex AI specific model.
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    embeddings = model.get_embeddings(audit_notes)
    
    return [embedding.values for embedding in embeddings]
