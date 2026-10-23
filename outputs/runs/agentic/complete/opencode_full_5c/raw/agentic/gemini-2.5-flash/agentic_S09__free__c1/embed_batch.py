import os
from typing import List
from embeddings_client import initialize_vertex_ai, get_embedding_model
from embeddings_models import prepare_texts_for_embedding, normalize_embedding_response


def embed_batch_texts(texts: List[str]) -> List[List[float]]:
    """
    Generates embedding vectors for a batch of text strings using Google Cloud Vertex AI.
    """
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    initialize_vertex_ai(project, location)
    model = get_embedding_model()

    inputs = prepare_texts_for_embedding(texts)
    embeddings_response = model.get_embeddings(inputs)

    return normalize_embedding_response(embeddings_response)
