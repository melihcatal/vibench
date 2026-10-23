import os
from dashscope import Embeddings

DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

def moderation_reason_embedding(text):
    embeddings = Embeddings(api_key=DASHSCOPE_API_KEY)
    response = embeddings.create_embedding(model='text-embedding-v1', input=text)
    return response.embeddings