import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embeddings_client():
    return openai.Embedding

def embed_text(text):
    response = openai.Embedding.create(input=text, model='text-embedding-ada-002')
    return response

def embed_batch(texts):
    response = openai.Embedding.create(input=texts, model='text-embedding-ada-002')
    return response