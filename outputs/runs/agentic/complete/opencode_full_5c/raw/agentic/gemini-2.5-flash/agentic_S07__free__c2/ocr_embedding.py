from document_client import get_aiplatform_client, get_project_id, get_location
from google.cloud.aiplatform.gapic.schema import predict_v1 as gapic_predict_v1
from google.protobuf import json_format
import json


def embed_document_section(text: str) -> list[float]:
    client = get_aiplatform_client()
    project_id = get_project_id()
    location = get_location()

    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/text-embedding-004"

    instance = gapic_predict_v1.instance.TextEmbeddingPredictionInstance(content=text)
    instances = [
        json_format.ParseDict(instance.to_dict(), google.protobuf.struct_pb2.Value())
    ]

    response = client.predict(endpoint=endpoint, instances=instances)

    # The prediction results for text embeddings usually contain an embedding field.
    # Extracting the embedding vector from the first prediction result.
    if response.predictions and response.predictions[0]:
        embedding_value = response.predictions[0]["embeddings"]
        if isinstance(embedding_value, dict) and "values" in embedding_value:
            return list(embedding_value["values"])
    return []
