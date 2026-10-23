import os
from typing import List, Tuple
from embeddings_client import initialize_vertex_ai, get_embedding_model
from embeddings_models import prepare_texts_for_embedding, normalize_embedding_response
from vertexai.language_models import TextEmbeddingInput


def embed_for_semantic_search(
    query: str, documents: List[str]
) -> Tuple[List[float], List[List[float]]]:
    """
    Embeds a query and a list of documents for semantic search using Google Cloud Vertex AI.
    The query is embedded with a 'QUESTION_ANSWERING' task type, and documents with 'RETRIEVAL_DOCUMENT'.
    """
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    initialize_vertex_ai(project, location)
    model = get_embedding_model()

    query_input = TextEmbeddingInput(query, "QUESTION_ANSWERING")
    document_inputs = [
        TextEmbeddingInput(doc, "RETRIEVAL_DOCUMENT") for doc in documents
    ]

    all_inputs = [query_input] + document_inputs
    embeddings_response = model.get_embeddings(all_inputs)

    normalized_embeddings = normalize_embedding_response(embeddings_response)

    query_embedding = normalized_embeddings[0]
    document_embeddings = normalized_embeddings[1:]

    return query_embedding, document_embeddings
