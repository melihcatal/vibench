import os
import openai

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def moderation_reason_embedding(text):
    openai.api_key = OPENAI_API_KEY
    response = openai.Embedding.create(input=text, model='text-embedding-ada-002')
    return response['data'][0]['embedding']