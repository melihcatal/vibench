import os
from cohere import Client

client = Client(os.getenv('COHERE_API_KEY'))

def embed_for_search(query, documents):
    query_embedding = client.embed(texts=[query]).embeddings[0]
    document_embeddings = client.embed(texts=documents).embeddings
    similarities = [sum(qe * de for qe, de in zip(query_embedding, doc_emb)) / (sum(qe**2 for qe in query_embedding) * sum(de**2 for de in doc_emb))**0.5 for doc_emb in document_embeddings]
    return similarities

if __name__ == '__main__':
    print(embed_for_search('sample query', ['sample document 1', 'sample document 2']))