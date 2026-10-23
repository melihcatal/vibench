import os
from typing import List
from google.cloud import aiplatform
from google.protobuf import value
from safety_client import GoogleSafetyClient


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_id = "text-embedding-004"  # A text embedding model

    client = GoogleSafetyClient(project_id, location)
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    instances = []
    for rationale in rationales:
        instance = value.Value()
        instance.struct_value.fields["text"].string_value = rationale
        instances.append(instance)

    parameters = value.Value()  # No specific parameters for text embedding usually needed beyond the text itself.

    response = client.vertex_ai_client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )

    embeddings: List[List[float]] = []
    for prediction in response.predictions:
        embedding_values = [
            field.number_value
            for field in prediction.struct_value.fields["embeddings"].list_value.values
        ]
        embeddings.append(embedding_values)

    return embeddings
