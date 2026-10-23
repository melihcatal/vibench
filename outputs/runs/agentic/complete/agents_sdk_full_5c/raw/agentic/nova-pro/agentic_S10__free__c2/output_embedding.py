import os
from sentence_transformers import SentenceTransformer

def embed_output(text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    return model.encode(text)