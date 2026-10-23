import os
from dashscope import TextEmbedding

def embed_translation_memory(text):
    api_key = os.getenv('DASHSCOPE_API_KEY')
    response = TextEmbedding.call(model='text-embedding-v1', input=text, api_key=api_key)
    return response.output.embeddings[0].embedding