import os
from typing import List
from google.cloud import aiplatform

def embed_translated_segment(translated_segment: str) -> List[float]:
    """Embeds a translated text segment for translation-memory search using Vertex AI Embeddings API.

    Args:
        translated_segment: The translated text segment to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID environment variable not set. "
            "Please set it to your Google Cloud Project ID."
        )

    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1") # Default to us-central1
    aiplatform.init(project=project_id, location=location)

    # Using the text-multilingual-embedding-002 model for multilingual text
    # See https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-text-embeddings
    model_id = "text-multilingual-embedding-002"
    try:
        model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)
    except Exception as e:
        # Fallback to text-embedding-004 if multilingual is not available or causes issues
        model_id = "text-embedding-004"
        model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)
        print(f"Warning: Using {model_id} as text-multilingual-embedding-002 failed to load: {e}")

    embeddings = model.get_embeddings([translated_segment])
    return embeddings[0].values
