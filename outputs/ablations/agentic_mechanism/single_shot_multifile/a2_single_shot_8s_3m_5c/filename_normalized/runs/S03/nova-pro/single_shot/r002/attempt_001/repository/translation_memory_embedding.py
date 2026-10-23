import os
from sentence_transformers import SentenceTransformer

def embed_translation_memory(text):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embedding = model.encode(text)
    return embedding.tolist()