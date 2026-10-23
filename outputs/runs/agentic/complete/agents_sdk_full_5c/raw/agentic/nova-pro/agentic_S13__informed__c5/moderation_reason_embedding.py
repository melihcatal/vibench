from cohere import Client

client = Client('COHERE_API_KEY')

def moderation_reason_embedding(text):
    response = client.embed(texts=[text])
    return response.embeddings[0]
