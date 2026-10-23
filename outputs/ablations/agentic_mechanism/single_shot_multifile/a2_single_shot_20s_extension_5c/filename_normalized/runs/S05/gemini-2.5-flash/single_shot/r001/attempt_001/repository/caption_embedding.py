import os
import vertexai
from vertexai.preview.language_models import TextEmbeddingModel

def embed_caption_chunk(caption_chunk_text, project_id=None, location=None):
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if location is None:
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id or not location:
        raise ValueError("Google Cloud project ID and location must be provided or set in environment variables (GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION).")

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings([caption_chunk_text])

    if embeddings and embeddings[0].values:
        return embeddings[0].values
    return []