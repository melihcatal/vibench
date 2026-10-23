import os
import cohere

os.environ['COHERE_API_KEY'] = 'your-cohere-api-key'

client = cohere.Client()

def embed_caption(text):
    response = client.embed(texts=[text])
    return response.embeddings[0]
