import os
import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_caption_chunk(caption_chunk: str, project_id: str = None, location: str = "us-central1", model_name: str = "text-embedding-004") -> list[float]:
    """Embeds a caption chunk for semantic meeting search using Vertex AI's embedding models."""
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained(model_name)

    embeddings = model.get_embeddings([caption_chunk])

    if embeddings and embeddings[0].values:
        embedding_values = embeddings[0].values
        print(f"Generated embedding for '{caption_chunk[:50]}...' (first 5 values): {embedding_values[:5]}...")
        return embedding_values
    else:
        print(f"Could not generate embedding for '{caption_chunk}'")
        return []
