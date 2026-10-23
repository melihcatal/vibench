from cohere.client import Client

def asset_metadata_embedding(text):
    client = Client('your-cohere-api-key')
    response = client.embed(texts=[text])
    return response.embeddings[0]