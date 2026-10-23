import os
import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_caption_chunk(
    text_chunk: str,
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id"),
    location: str = "us-central1"
) -> list[float]:
    """Embeds caption chunks for semantic meeting search using Google's Generative AI (Vertex AI)."""

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

    embeddings = model.get_embeddings([text_chunk])
    return embeddings[0].values
