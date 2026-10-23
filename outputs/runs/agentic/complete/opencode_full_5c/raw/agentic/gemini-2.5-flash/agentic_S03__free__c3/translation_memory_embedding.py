from google.cloud import aiplatform
from translation_models import get_project_id, get_location
from typing import List

# Vertex AI model for text embeddings
# Choose an appropriate model, e.g., "text-embedding-004"
EMBEDDING_MODEL_NAME = "text-embedding-004"


def get_text_embeddings(texts: List[str]) -> List[List[float]]:
    """Generates text embeddings for translated segments using Google Cloud Vertex AI.

    These embeddings can be used for similarity search in a translation memory system.

    Args:
        texts: A list of text segments to embed.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    project_id = get_project_id()
    location = get_location()

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL_NAME)

    # The predict method takes a list of texts and returns a list of embeddings
    embeddings = model.predict(texts).embeddings

    # Extract the embedding vectors from the Embedding objects
    embedding_vectors = [embedding.values for embedding in embeddings]

    return embedding_vectors
