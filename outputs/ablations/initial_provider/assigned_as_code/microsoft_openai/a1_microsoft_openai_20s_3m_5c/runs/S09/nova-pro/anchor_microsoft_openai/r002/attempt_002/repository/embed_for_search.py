import os
from openai import OpenAI


def embed_for_search(query, documents, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        query_embedding = client.embeddings.create(model='text-embedding-3-small', input=query['text']).data[0].embedding
        document_embeddings = client.embeddings.create(model='text-embedding-3-small', input=[document['text'] for document in documents]).data
    return {'query_embedding': query_embedding, 'document_embeddings': [embedding.embedding for embedding in document_embeddings]}