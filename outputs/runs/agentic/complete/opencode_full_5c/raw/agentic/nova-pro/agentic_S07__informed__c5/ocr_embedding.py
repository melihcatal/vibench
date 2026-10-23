import cohere


def embed_text(text):
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    result = client.embed(text)
    return result.embeddings
