from cohere.client import Client


def embed_output(text):
    client = Client(api_key=os.getenv("COHERE_API_KEY"))
    response = client.embed(texts=[text])
    return response.embeddings[0]
