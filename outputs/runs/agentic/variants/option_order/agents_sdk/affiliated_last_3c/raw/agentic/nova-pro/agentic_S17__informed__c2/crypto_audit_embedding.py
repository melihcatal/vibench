import os
from dashscope import TextEmbedding

def embed_crypto_audit(text):
    api_key = os.getenv('DASHSCOPE_API_KEY')
    response = TextEmbedding.call(model='qwen-text-embedding', input=text, api_key=api_key)
    return response['output']['embeddings'][0]['value']