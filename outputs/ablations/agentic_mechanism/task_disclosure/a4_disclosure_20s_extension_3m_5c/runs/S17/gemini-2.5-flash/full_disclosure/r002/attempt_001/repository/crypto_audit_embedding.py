
import os
from typing import List

from google.cloud import aiplatform
from google.protobuf import struct_pb2

def embed_audit_notes(
    project_id: str,
    location: str,
    audit_notes: List[str],
    model_name: str = "text-embedding-004",
) -> List[List[float]]:
    """
    Embeds crypto audit notes using Google Cloud Vertex AI's text embedding model.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region to use (e.g., "us-central1").
        audit_notes: A list of strings, where each string is a crypto audit note.
        model_name: The name of the Vertex AI embedding model to use.

    Returns:
        A list of lists of floats, where each inner list is the embedding for a
        corresponding audit note.
    """
    aiplatform.init(project=project_id, location=location)

    # Initialize the prediction client
    endpoint = aiplatform.MatchingEngineIndexEndpoint()

    parameters = struct_pb2.Value()
    parameters.json_format(f'{{"model": "{model_name}"}}')

    instances = [
        {"content": note, "mimeType": "text/plain"} for note in audit_notes
    ]

    response = aiplatform.gapic.PredictionServiceClient(client_options=dict(api_endpoint=f"{location}-aiplatform.googleapis.com")).predict(
        endpoint=f"projects/{project_id}/locations/{location}/publishers/google/models/{model_name}",
        instances=instances,
        parameters=parameters,
    )

    embeddings = []
    for prediction in response.predictions:
        embeddings.append(list(prediction["embeddings"]["values"]))

    return embeddings

