import os
from typing import List
from embeddings_client import initialize_vertex_ai, get_embedding_model
from embeddings_models import prepare_texts_for_embedding, normalize_embedding_response


def embed_single_text(text: str) -> List[float]:
    """
    Generates an embedding vector for a single text string using Google Cloud Vertex AI.
    """
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    initialize_vertex_ai(project, location)
    model = get_embedding_model()

    inputs = prepare_texts_for_embedding([text])
    embeddings_response = model.get_embeddings(inputs)

    # The response contains a list of embeddings, take the first one for a single text
    normalized_embeddings = normalize_embedding_response(embeddings_response)
    return normalized_embeddings[0]
