import os
import google.cloud.aiplatform as aiplatform

def embed_text(text: str) -> list[float]:
    """
    Embeds model outputs using Google Cloud Vertex AI's text-embedding-004 model.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    
    aiplatform.init(project=project_id, location="us-central1") # Using us-central1 as a common region for Vertex AI

    # The text-embedding-004 model is available through the TextEmbeddingModel class
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([text])
    
    # Assuming one text input, so we take the first embedding
    if embeddings and embeddings[0].values:
        return embeddings[0].values
    return []

