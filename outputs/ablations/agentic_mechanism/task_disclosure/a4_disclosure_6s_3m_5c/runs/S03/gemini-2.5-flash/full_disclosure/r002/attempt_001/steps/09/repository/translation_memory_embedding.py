import os
from typing import List

from google.cloud import aiplatform
from google.protobuf import struct_pb2

def embed_translated_segments(
    project: str,
    location: str,
    segments: List[str],
) -> List[List[float]]:
    """Embeds translated segments using Google Cloud's Vertex AI Embeddings API.

    Args:
        project: Your Google Cloud project ID.
        location: The region of the Vertex AI endpoint (e.g., "us-central1").
        segments: A list of translated text segments to embed.

    Returns:
        A list of embedding vectors, where each vector corresponds to a segment.
    """
    aiplatform.init(project=project, location=location)

    # The `text-embedding-004` model is a concrete identifier for Google Cloud.
    model = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )
    endpoint = f"projects/{project}/locations/{location}/publishers/google/models/text-embedding-004"

    instances = []
    for segment in segments:
        instances.append(
            struct_pb2.Value(
                struct_value=struct_pb2.Struct(
                    fields={
                        "text": struct_pb2.Value(string_value=segment),
                    }
                )
            )
        )

    response = model.predict(endpoint=endpoint, instances=instances)
    
    embeddings = []
    for prediction in response.predictions:
        embeddings.append(list(prediction["embeddings"]))
    
    return embeddings

