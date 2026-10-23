import os
from google.cloud import embeddings_v1

def embed_for_search(query, documents):
    api_endpoint = 'us-central1-aiplatform.googleapis.com'
    client_options = {"api_endpoint": api_endpoint}
    client = embeddings_v1.EmbeddingServiceClient(client_options=client_options)
    parent = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/us-central1'
    query_request = embeddings_v1.GenerateEmbeddingRequest(
        parent=parent,
        content=[query],
        model='textembedding-gecko@001'
    )
    query_response = client.generate_embedding(request=query_request)
    query_embedding = query_response.embeddings[0].values
    doc_request = embeddings_v1.BatchGenerateEmbeddingsRequest(
        parent=parent,
        contents=documents,
        model='textembedding-gecko@001'
    )
    doc_response = client.batch_generate_embeddings(request=doc_request)
    doc_embeddings = [embedding.values for embedding in doc_response.embeddings]
    return query_embedding, doc_embeddings