import os
from google.cloud import aiplatform_v1 as aiplatform_v1_gapic
from google.protobuf import struct_pb2
from model_client import get_vertex_ai_embedding_model_client, get_vertex_ai_publisher_model_endpoint
from model_models import EmbeddingRequest, EmbeddingResponse, normalize_vertex_ai_embedding_response


def embed_output(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GCP_PROJECT_ID')
    location = config.get('location') or os.environ.get('GCP_LOCATION', 'us-central1')
    model_id = config.get('model_id') or 'text-embedding-004'

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    client = get_vertex_ai_embedding_model_client(project_id, location)
    endpoint = get_vertex_ai_publisher_model_endpoint(model_id)

    texts_to_embed = payload.get('texts', [])
    if not isinstance(texts_to_embed, list):
        texts_to_embed = [texts_to_embed]

    instances = []
    for text_entry in texts_to_embed:
        instance = struct_pb2.Value()
        instance.struct_value.fields["text"].string_value = text_entry
        instances.append(instance)

    response = client.predict(endpoint=endpoint, instances=instances)
    
    embedding_response = normalize_vertex_ai_embedding_response(response)
    
    return {'embeddings': embedding_response.embeddings}
