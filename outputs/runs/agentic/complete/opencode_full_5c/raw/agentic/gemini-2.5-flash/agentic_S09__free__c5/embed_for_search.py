import os
from typing import List, Tuple
from google.cloud.aiplatform_v1.types import PredictRequest

from embeddings_client import get_vertex_ai_prediction_client
from embeddings_models import (
    EMBEDDING_MODEL_TEXT,
    format_embed_request,
    parse_embed_response,
)


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[List[float], List[List[float]]]:
    """Embeds a query and documents for semantic search using Vertex AI.

    Args:
        query: The search query string.
        documents: A list of document strings.

    Returns:
        A tuple containing the query embedding and a list of document embeddings.
    """
    client = get_vertex_ai_prediction_client()
    project_id = os.environ.get("GCP_PROJECT_ID")

    endpoint_id = (
        EMBEDDING_MODEL_TEXT  # For text-embedding-004, the model ID is the endpoint ID
    )
    # The actual endpoint resource name should be in the format:
    # projects/<project_id>/locations/<location>/publishers/google/models/<model_id>
    endpoint = f"projects/{project_id}/locations/us-central1/publishers/google/models/{endpoint_id}"

    all_texts = [query] + documents
    request_payload = format_embed_request(all_texts, EMBEDDING_MODEL_TEXT)
    predict_request = PredictRequest(
        endpoint=endpoint, instances=request_payload["instances"]
    )

    response = client.predict(request=predict_request)
    embeddings = parse_embed_response(response)

    query_embedding = embeddings[0]
    document_embeddings = embeddings[1:]

    return query_embedding, document_embeddings
