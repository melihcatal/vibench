import os
from typing import List
from google.cloud.aiplatform_v1.types import PredictRequest

from embeddings_client import get_vertex_ai_prediction_client
from embeddings_models import (
    EMBEDDING_MODEL_TEXT,
    format_embed_request,
    parse_embed_response,
)


def embed_text(text: str) -> List[float]:
    """Generates an embedding vector for a single text string using Vertex AI.

    Args:
        text: The input text string.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = get_vertex_ai_prediction_client()
    project_id = os.environ.get("GCP_PROJECT_ID")

    endpoint_id = (
        EMBEDDING_MODEL_TEXT  # For text-embedding-004, the model ID is the endpoint ID
    )
    # The actual endpoint resource name should be in the format:
    # projects/<project_id>/locations/<location>/publishers/google/models/<model_id>
    endpoint = f"projects/{project_id}/locations/us-central1/publishers/google/models/{endpoint_id}"

    request_payload = format_embed_request([text], EMBEDDING_MODEL_TEXT)
    predict_request = PredictRequest(
        endpoint=endpoint, instances=request_payload["instances"]
    )

    response = client.predict(request=predict_request)
    embeddings = parse_embed_response(response)
    return embeddings[0]
