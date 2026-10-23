import os
from dashscope import TextEmbedding

def embed_script(text):
    response = TextEmbedding.call(model='text-embedding-v1', input=text)
    return response['output']['data'][0]['embedding']