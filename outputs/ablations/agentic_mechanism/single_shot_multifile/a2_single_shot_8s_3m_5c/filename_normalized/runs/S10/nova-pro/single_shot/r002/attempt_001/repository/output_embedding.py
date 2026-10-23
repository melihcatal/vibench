import os
from sentence_transformers import SentenceTransformer

def embed_output(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text)
    return embedding