import os
from huggingface_hub import InferenceClient

client = InferenceClient(token=os.getenv('HUGGINGFACE_API_KEY'))

def embed_batch(texts):
    embeddings = []
    for text in texts:
        response = client.text_embeddings(text, model='sentence-transformers/all-MiniLM-L6-v2')
        embeddings.append(response['embedding'])
    return embeddings