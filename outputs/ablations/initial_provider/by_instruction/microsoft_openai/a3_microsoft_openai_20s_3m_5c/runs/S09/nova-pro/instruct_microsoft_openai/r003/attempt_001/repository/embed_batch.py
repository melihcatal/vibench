from.embeddings_client import get_text_analytics_client

def embed_batch(texts):
    client = get_text_analytics_client()
    results = client.batch_embed(texts)
    return [result.embedding for result in results]

if __name__ == '__main__':
    print(embed_batch(['Hello, world!', 'Goodbye, world!']))