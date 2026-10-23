import os
from sentence_transformers import SentenceTransformer

def embed_text(text):
    model = SentenceTransformer(os.getenv('SENTENCE_TRANSFORMERS_MODEL'))
    embeddings = model.encode(text)
    return embeddings.tolist()