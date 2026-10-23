from google.cloud import aiplatform_v1 as aiplatform
from model_models import ModelInput
import json


def embed_vertex_ai_output(
    project_id: str,
    location: str,
    model_id: str,  # e.g., "text-embedding-gecko@001"
    text: str,
) -> list[float]:
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.PredictionServiceClient(client_options=client_options)

    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    instances = [{"content": text}]

    response = client.predict(endpoint=endpoint, instances=instances)

    embeddings = []
    for prediction in response.predictions:
        if "embeddings" in prediction and "values" in prediction["embeddings"]:
            embeddings.extend(prediction["embeddings"]["values"])

    return embeddings
