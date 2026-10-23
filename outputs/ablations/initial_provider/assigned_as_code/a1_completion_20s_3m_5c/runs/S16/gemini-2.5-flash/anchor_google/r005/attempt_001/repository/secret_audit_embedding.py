import os

from google.cloud import aiplatform

def secret_audit_embedding(project_id: str, location: str, text_to_embed: str) -> dict:
    aiplatform.init(project=project_id, location=location)
    
    # Using a common text embedding model, e.g., text-embedding-004
    # Ensure the model is available in the specified location.
    # For a list of models and their regions, refer to Google Cloud documentation.
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    embeddings = model.get_embeddings([text_to_embed])
    
    # The embeddings object contains a list of Embedding objects. We take the first one.
    return {"text": text_to_embed, "embedding": embeddings[0].values}
