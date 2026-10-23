import os
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from translation_client import get_vertex_ai_prediction_client

def embed_translated_segment(
    project_id: str,
    location: str,
    text_segment: str,
    model_id: str = "text-embedding-gecko",
) -> list[float]:
    """Embeds translated segments for translation-memory search using Google Cloud Vertex AI."""
    client = get_vertex_ai_prediction_client(api_endpoint=f"{location}-aiplatform.googleapis.com")
    endpoint = client.endpoint_path(
        project=project_id, location=location, publisher="google", model=model_id
    )

    instance = json_format.ParseDict(
        {"content": text_segment},
        Value(),
    )
    instances = [instance]

    response = client.predict(endpoint=endpoint, instances=instances)

    if response.predictions and "embeddings" in response.predictions[0]:
        return list(response.predictions[0]["embeddings"]["values"])
    return []

