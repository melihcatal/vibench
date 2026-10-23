import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def embed_text(text):
    response = client.embeddings.create(input=text, model='text-embedding-ada-002')
    return response.data[0].embedding