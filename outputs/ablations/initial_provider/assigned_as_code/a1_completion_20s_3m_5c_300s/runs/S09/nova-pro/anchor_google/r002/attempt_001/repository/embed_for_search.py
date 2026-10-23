import os
from huggingface_hub import InferenceApi

api = InferenceApi('sentence-transformers/all-MiniLM-L6-v2', token=os.getenv('HUGGING_FACE_API_KEY'))

def embed_for_search(query, documents):
    query_embedding = api(query)['data'][0]
    document_embeddings = api(documents)['data']
    return query_embedding, document_embeddings