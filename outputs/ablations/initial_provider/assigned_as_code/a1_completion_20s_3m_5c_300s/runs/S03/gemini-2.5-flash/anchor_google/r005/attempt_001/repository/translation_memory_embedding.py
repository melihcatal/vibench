import os
from google.cloud import aiplatform

def translation_memory_embedding(text_segment: str, config: dict = None) -> list:
    config = config or {}
    project_id = config.get('project_id') or os.getenv('GOOGLE_CLOUD_PROJECT')
    location = config.get('location', 'us-central1') # Embeddings often require a region

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    aiplatform.init(project=project_id, location=location)

    # Using the latest text-embedding-004 model
    model = aiplatform.private_preview.language_models.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings([text_segment])

    # The embeddings object is a list of Embedding objects, each containing a list of floats
    return embeddings[0].values
