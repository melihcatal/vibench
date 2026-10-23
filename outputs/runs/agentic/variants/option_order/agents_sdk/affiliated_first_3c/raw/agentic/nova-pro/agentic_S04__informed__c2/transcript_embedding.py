import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def transcript_embedding(text):
    response = openai.Embedding.create(input=text, model='text-embedding-ada-002')
    return response['data'][0]['embedding']