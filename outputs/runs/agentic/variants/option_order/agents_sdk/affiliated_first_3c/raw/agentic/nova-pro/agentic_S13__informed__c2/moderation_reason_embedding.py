import os
from openai import OpenAI

def moderation_reason_embedding(text):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(input=text, model='text-embedding-ada-002')
    return response.data[0].embedding