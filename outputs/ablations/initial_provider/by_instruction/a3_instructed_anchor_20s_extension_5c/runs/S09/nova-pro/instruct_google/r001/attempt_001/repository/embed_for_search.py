from google.cloud import aiplatform

def embed_for_search(query, documents):
    client = aiplatform.gapic.PredictionServiceClient()
    model_name = 'projects/1234567890/locations/us-central1/models/text-embedding-v1'
    instances = [{'content': doc} for doc in documents] + [{'content': query}]
    response = client.predict(name=model_name, instances=instances)
    embeddings = [pred['embedding'] for pred in response.predictions]
    return embeddings[-1], embeddings[:-1]