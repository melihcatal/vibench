import os
from google.cloud import aiplatform

def get_text_embeddings(text: str) -> list[float]:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    # The model_id for text embeddings. For example, "text-embedding-004" or "text-embedding-preview-0409".
    # This should be replaced with an actual deployed embedding model if using a custom one.
    # For public models, you can use the TextEmbeddingModel class directly.
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings([text])
    
    # The get_embeddings method returns a list of objects, each containing an embedding.
    # We extract the values from the first embedding result.
    return embeddings[0].values