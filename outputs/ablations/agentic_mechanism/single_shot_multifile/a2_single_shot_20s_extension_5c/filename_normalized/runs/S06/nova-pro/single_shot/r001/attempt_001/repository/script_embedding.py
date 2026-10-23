import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_script(text):
    embeddings = model.encode(text)
    return embeddings