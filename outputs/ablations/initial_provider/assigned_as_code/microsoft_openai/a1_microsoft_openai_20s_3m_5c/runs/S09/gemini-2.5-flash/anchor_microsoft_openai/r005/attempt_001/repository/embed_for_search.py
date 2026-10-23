import os
from openai import OpenAI


def embed_for_search(payload, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        query_response = client.embeddings.create(model='text-embedding-3-small', input=payload['query'])
        documents_response = client.embeddings.create(model='text-embedding-3-small', input=payload['documents'])
    
    return {
        'query_embedding': query_response.data[0].embedding,
        'document_embeddings': [item.embedding for item in documents_response.data]
    }