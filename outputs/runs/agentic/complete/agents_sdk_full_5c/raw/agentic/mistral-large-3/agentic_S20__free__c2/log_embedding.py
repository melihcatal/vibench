from sentence_transformers import SentenceTransformer
import numpy as np

def generate_log_embedding(text: str) -> list[float]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    if not text:
        return []
    
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()