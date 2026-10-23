import cohere


def embed_translation_memory(text):
    api_key = os.getenv("COHERE_API_KEY")
    client = cohere.Client(api_key)
    response = client.embed(texts=[text])
    return response.embeddings[0]
