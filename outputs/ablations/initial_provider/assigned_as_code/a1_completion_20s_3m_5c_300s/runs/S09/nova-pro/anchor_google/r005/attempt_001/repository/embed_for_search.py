import os

from google import genai


def embed_for_search(query, documents, config=None):
    config = config or {}
    with genai.Client(api_key=config.get('api_key') or os.environ['GOOGLE_API_KEY']) as client:
        query_embedding = client.models.embed_content(model='gemini-embedding-001', contents=query)['embedding']
        document_embeddings = [client.models.embed_content(model='gemini-embedding-001', contents=doc)['embedding'] for doc in documents]
    return query_embedding, document_embeddings