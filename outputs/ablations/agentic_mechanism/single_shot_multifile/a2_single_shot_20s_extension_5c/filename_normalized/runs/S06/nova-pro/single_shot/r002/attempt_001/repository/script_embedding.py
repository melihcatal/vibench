import os
from sentence_transformers import SentenceTransformer

def embed_script(text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding = model.encode(text)
    return embedding