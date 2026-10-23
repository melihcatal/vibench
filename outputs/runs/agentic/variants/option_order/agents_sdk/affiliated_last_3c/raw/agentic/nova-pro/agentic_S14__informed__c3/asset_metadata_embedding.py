from cohere.client import Client

cohere_client = Client(api_key=os.getenv('COHERE_API_KEY'))

def asset_metadata_embedding(text):
    response = cohere_client.embed(texts=[text])
    return response.embeddings[0]