import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed_moderation_reason(reason):
    embedding = model.encode(reason)
    return embedding