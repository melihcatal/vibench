import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def transcript_embedding(transcript_text):
    response = client.embeddings.create(input=transcript_text, model='text-embedding-ada-002')
    return response.data[0].embedding