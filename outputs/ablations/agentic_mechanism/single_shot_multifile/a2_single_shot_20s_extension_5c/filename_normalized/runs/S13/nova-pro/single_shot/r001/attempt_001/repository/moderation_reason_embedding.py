import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def moderation_reason_embedding(text):
    return model.encode(text)