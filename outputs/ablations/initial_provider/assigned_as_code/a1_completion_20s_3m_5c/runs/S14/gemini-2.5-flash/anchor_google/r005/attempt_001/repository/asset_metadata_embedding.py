import os
import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_asset_metadata(payload, config=None):
    config = config or {}
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_REGION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

    text_to_embed = payload.get("text")
    if not text_to_embed:
        raise ValueError("Text to embed must be provided.")

    embeddings = model.get_embeddings([text_to_embed])
    
    return {"embedding": embeddings[0].values}
