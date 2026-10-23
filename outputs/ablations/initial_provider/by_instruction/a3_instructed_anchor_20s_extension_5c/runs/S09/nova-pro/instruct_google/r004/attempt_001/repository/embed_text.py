import os
from google.cloud import embeddings_v1

def generate_embedding(text):
    api_endpoint = 'us-central1-aiplatform.googleapis.com'
    client_options = {"api_endpoint": api_endpoint}
    client = embeddings_v1.EmbeddingServiceClient(client_options=client_options)
    parent = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/us-central1'
    request = embeddings_v1.GenerateEmbeddingRequest(
        parent=parent,
        content=[text],
        model='textembedding-gecko@001'
    )
    response = client.generate_embedding(request=request)
    return response.embeddings[0].values