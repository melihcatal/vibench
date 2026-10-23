import os
from dashscope import TextEmbedding

def embed_crypto_audit(text):
    api_key = os.getenv('DASHSCOPE_API_KEY')
    response = TextEmbedding.call(model='text-embedding-v1', input=text, api_key=api_key)
    return response['output']['embeddings'][0]['vector']

# Example usage (uncomment to test):
# embedding = embed_crypto_audit('your-text')