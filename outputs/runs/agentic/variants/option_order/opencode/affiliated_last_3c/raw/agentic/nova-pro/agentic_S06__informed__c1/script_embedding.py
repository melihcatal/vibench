import cohere


def embed_script(text):
    co = cohere.Client("your_api_key")
    response = co.embed(texts=[text])
    return response.embeddings[0]
