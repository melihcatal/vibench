from.embeddings_client import get_text_analytics_client

def embed_text(text):
    client = get_text_analytics_client()
    result = client.single_embed(text)
    return result.embedding

if __name__ == '__main__':
    print(embed_text('Hello, world!'))