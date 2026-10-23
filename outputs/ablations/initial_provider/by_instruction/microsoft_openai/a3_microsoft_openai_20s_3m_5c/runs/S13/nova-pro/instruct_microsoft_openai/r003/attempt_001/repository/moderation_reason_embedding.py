import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def embed_rationale(text):
    response = openai.Embedding.create(input=text)
    return response.data[0].embedding