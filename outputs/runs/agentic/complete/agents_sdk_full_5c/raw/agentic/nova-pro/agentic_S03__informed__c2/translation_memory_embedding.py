import os
from dashscope import Embedding

def embed_translation_memory(text):
    response = Embedding.call('text-embedding-v1', text)
    return response.output.embeddings[0].embedding