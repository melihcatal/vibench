import boto3
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    embeddings = model.encode(text)
    return np.array(embeddings)