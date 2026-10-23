import os
from google.cloud import embeddings_v1

def get_embeddings_client():
    api_endpoint = 'us-central1-aiplatform.googleapis.com'
    client_options = {"api_endpoint": api_endpoint}
    client = embeddings_v1.EmbeddingServiceClient(client_options=client_options)
    return client

def get_parent():
    return f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/us-central1'