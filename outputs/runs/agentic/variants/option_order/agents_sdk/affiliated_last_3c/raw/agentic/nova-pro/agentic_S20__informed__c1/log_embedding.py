import os
import cohere

co = cohere.Client(os.getenv('COHERE_API_KEY'))

def embed_message(message):
    response = co.embed(texts=[message])
    return response.embeddings[0]

message = 'This is an example log message.'
embedding = embed_message(message)
print(embedding)