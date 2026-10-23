import os
from cohere import Client

co = Client(os.getenv('COHERE_API_KEY'))

def embed_for_search(query, documents):
    query_embedding = co.embed(texts=[query]).embeddings[0]
    document_embeddings = co.embed(texts=documents).embeddings
    return query_embedding, document_embeddings
