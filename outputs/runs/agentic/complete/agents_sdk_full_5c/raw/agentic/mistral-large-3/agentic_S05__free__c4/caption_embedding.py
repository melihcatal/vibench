from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_caption(caption: str) -> np.ndarray:
    embedding = model.encode(caption, convert_to_numpy=True)
    return embedding