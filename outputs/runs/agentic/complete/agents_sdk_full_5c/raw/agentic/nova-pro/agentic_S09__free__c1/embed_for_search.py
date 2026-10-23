import os
from huggingface_hub import InferenceClient

client = InferenceClient(token=os.getenv('HUGGINGFACE_API_KEY'))

def embed_for_search(query, documents):
    query_embedding = client.text_embeddings(query, model='sentence-transformers/all-MiniLM-L6-v2')['embedding']
    document_embeddings = [client.text_embeddings(doc, model='sentence-transformers/all-MiniLM-L6-v2')['embedding'] for doc in documents]
    return query_embedding, document_embeddings