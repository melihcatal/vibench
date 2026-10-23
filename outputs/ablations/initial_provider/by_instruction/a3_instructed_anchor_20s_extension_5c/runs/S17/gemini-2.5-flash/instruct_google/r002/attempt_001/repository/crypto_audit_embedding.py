import os
from google.cloud import aiplatform

def embed_audit_note(project_id: str, location: str, text: str) -> list[float]:
    aiplatform.init(project=project_id, location=location)
    
    # Use a pre-trained text embedding model
    # The model name should be specific, e.g., 'text-embedding-004'
    # Refer to Google Cloud Vertex AI documentation for available models.
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("text-embedding-gecko@003")

    embeddings = model.get_embeddings([text])
    return embeddings[0].values
