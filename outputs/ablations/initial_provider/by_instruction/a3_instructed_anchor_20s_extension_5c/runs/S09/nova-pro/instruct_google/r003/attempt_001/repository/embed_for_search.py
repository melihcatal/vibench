import os
from google.cloud import aiplatform

def embed_for_search(query, documents):
    aiplatform.init(project='your-project-id')
    model = aiplatform.PredictionServiceClient()
    query_embedding = model.predict(
        endpoint='your-endpoint-id',
        instances=[{"content": query}]
    ).predictions[0]['outputs'][0]['embedding']
    document_embeddings = model.predict(
        endpoint='your-endpoint-id',
        instances=[{"content": doc} for doc in documents]
    ).predictions
    document_embeddings = [pred['outputs'][0]['embedding'] for pred in document_embeddings]
    return query_embedding, document_embeddings