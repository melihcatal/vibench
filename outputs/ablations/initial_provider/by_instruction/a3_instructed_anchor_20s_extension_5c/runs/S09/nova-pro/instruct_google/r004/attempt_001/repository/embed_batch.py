import os
from google.cloud import embeddings_v1

def generate_embeddings(texts):
    api_endpoint = 'us-central1-aiplatform.googleapis.com'
    client_options = {"api_endpoint": api_endpoint}
    client = embeddings_v1.EmbeddingServiceClient(client_options=client_options)
    parent = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/us-central1'
    request = embeddings_v1.BatchGenerateEmbeddingsRequest(
        parent=parent,
        contents=texts,
        model='textembedding-gecko@001'
    )
    response = client.batch_generate_embeddings(request=request)
    return [embedding.values for embedding in response.embeddings]