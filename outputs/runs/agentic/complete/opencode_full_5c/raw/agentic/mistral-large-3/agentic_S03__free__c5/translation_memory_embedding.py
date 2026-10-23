from typing import List
import os
from google.cloud import aiplatform
from google.protobuf import struct_pb2


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    """
    Embeds translated segments for translation-memory search using Google Cloud Vertex AI.
    Uses the textembedding-gecko@latest model for embeddings.
    """
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"), location="us-central1"
    )

    if not os.getenv("GOOGLE_CLOUD_PROJECT_ID"):
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")

    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    endpoint = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/us-central1/publishers/google/models/textembedding-gecko@latest"

    instances = [struct_pb2.Value(string_value=segment) for segment in segments]
    instances = [
        struct_pb2.Value(struct_value=struct_pb2.Struct(fields={"content": instance}))
        for instance in instances
    ]

    response = client.predict(endpoint=endpoint, instances=instances)

    embeddings = []
    for prediction in response.predictions:
        embedding = prediction["embeddings"]["values"]
        embeddings.append(embedding)

    return embeddings
