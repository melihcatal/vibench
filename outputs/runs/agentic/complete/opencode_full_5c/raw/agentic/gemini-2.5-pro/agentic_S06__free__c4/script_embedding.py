import os
from speech_client import get_aiplatform_client
from speech_models import EmbeddingRequest, EmbeddingResponse
from google.cloud.aiplatform.gapic.preview import PredictionServiceClient
from google.api_core import client_options


def script_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    endpoint_id = "text-embedding-004"

    client_options_val = client_options.ClientOptions(
        api_endpoint=f"{location}-aiplatform.googleapis.com"
    )

    prediction_client = PredictionServiceClient(client_options=client_options_val)

    endpoint = f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}"

    instances = [{"content": request.text}]

    response = prediction_client.predict(endpoint=endpoint, instances=instances)

    embedding = response.predictions[0]["embeddings"]["values"]

    return EmbeddingResponse(embedding=embedding)
