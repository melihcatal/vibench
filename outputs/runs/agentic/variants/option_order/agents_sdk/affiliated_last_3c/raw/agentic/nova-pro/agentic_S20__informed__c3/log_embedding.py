import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def embed_log(log_text):
    response = openai.Embedding.create(input=log_text, model='text-embedding-ada-002')
    return response['data'][0]['embedding']