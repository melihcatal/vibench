import os
import cohere

client = cohere.Client(os.getenv('COHERE_API_KEY'))

response = client.embed(
    texts=['Hello, world!'],
    model='large'
)
print(response.embeddings)