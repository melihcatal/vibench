import os
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from google.cloud.aiplatform_v1beta1.types import PredictRequest
from google.cloud.aiplatform_v1beta1.services.prediction_service import PredictionServiceClient

def output_embedding(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = config.get('location') or os.environ.get('GOOGLE_CLOUD_LOCATION')
    model_name = config.get('model_name') or 'text-embedding-004' # Google Cloud Text Embedding model

    client_options = {'api_endpoint': f'{location}-aiplatform.googleapis.com'}
    client = PredictionServiceClient(client_options=client_options)

    endpoint = client.endpoint_path(
        project=project_id,
        location=location,
        publisher='google',
        model=model_name
    )

    instances_data = [{'text_content': payload['text']}]
    
    # Convert Python dicts to protobuf Value objects
    instances_pb = [json_format.ParseDict(instance, Value()) for instance in instances_data]

    request = PredictRequest(
        endpoint=endpoint,
        instances=instances_pb
    )

    response = client.predict(request=request)

    embeddings = []
    for prediction in response.predictions:
        # Assuming each prediction has an 'embeddings' key with a 'values' list
        if 'embeddings' in prediction and 'values' in prediction['embeddings']:
            embeddings.append(list(prediction['embeddings']['values']))
    
    return {'embeddings': embeddings, 'text': payload['text']}
