import os
from sentence_transformers import SentenceTransformer

def get_embedding_model():
    return SentenceTransformer('paraphrase-MiniLM-L6-v2')

def embed_translated_segments(segments):
    model = get_embedding_model()
    embeddings = model.encode(segments)
    return embeddings
