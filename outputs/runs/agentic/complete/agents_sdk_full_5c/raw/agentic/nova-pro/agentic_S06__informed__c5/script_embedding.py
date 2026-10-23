import cohere

def embed_script(text):
    client = cohere.Client('COHERE_API_KEY')
    response = client.embed(texts=[text])
    return response.embeddings[0]