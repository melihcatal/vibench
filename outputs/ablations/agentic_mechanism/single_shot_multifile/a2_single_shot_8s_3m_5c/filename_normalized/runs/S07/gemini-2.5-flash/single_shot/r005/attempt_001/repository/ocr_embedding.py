import os
from document_client import get_aiplatform_prediction_client
from document_models import EmbeddingResponse
from google.cloud.aiplatform_v1.types import endpoint as aiplatform_endpoint
from google.cloud.aiplatform_v1.types import predict_service as aiplatform_predict_service
from google.protobuf import struct_pb2

def embed_document_sections(texts: list[str]) -> list[EmbeddingResponse]:
    client = get_aiplatform_prediction_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")

    if not all([project_id, location]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID or GOOGLE_CLOUD_LOCATION environment variables.")

    # Model ID for text embeddings
    model_id = "text-embedding-004" # or text-embedding-gecko@003
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    instances = []
    for text in texts:
        instance = struct_pb2.Value()
        instance.struct_value.fields["text_content"].string_value = text
        instances.append(instance)
    
    parameters = struct_pb2.Value()
    parameters.struct_value.fields["auto_truncate"].bool_value = True

    request = aiplatform_predict_service.PredictRequest(
        endpoint=endpoint,
        instances=instances,
        parameters=parameters
    )

    response = client.predict(request=request)

    embedding_responses = []
    if response.predictions:
        for prediction_data in response.predictions:
            # Each prediction data contains an 'embeddings' field which is a list of floats
            if 'embeddings' in prediction_data and 'values' in prediction_data['embeddings']:
                embedding_responses.append(EmbeddingResponse(embeddings=list(prediction_data['embeddings']['values'])))
            else:
                embedding_responses.append(EmbeddingResponse(embeddings=[]))

    return embedding_responses
