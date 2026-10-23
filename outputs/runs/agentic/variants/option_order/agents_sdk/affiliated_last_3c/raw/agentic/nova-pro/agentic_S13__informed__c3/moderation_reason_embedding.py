import os
import openai

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def moderation_reason_embedding(reason):
    openai.api_key = OPENAI_API_KEY
    response = openai.Embedding.create(input=reason, model='text-embedding-ada-002')
    return response['data'][0]['embedding']