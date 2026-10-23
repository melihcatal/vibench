import os
from dashscope import TextEmbedding

DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

def embed_secret_audit_notes(text):
    response = TextEmbedding.call(model='text-embedding-v1', input=text)
    return response['output']['embeddings'][0]['embedding']