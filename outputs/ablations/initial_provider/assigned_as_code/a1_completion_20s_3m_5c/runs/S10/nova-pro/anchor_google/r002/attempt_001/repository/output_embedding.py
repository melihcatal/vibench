import os
from sentence_transformers import SentenceTransformer


def embed_output(payload):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(payload["text"])
    return {"embedding": embedding.tolist()}