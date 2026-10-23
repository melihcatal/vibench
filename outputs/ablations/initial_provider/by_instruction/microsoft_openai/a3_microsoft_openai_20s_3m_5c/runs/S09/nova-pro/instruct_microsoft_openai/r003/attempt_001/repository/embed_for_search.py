from.embeddings_client import get_text_analytics_client

def embed_for_search(query, documents):
    client = get_text_analytics_client()
    query_embedding = client.single_embed(query).embedding
    document_embeddings = [client.single_embed(doc).embedding for doc in documents]
    return query_embedding, document_embeddings

if __name__ == '__main__':
    print(embed_for_search('Hello, world!', ['Hello, world!', 'Goodbye, world!']))