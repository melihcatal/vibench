import os
import openai

openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

def transcript_embedding(text):
    response = openai.Embedding.create(model='text-embedding-ada-002', input=text)
    return response['data'][0]['embedding']