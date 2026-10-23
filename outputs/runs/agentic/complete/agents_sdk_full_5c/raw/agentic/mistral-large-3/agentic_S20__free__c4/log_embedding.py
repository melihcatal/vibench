from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

def embed_log_messages(messages: List[str]) -> List[List[float]]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(messages, convert_to_numpy=True)
    return np.array(embeddings).tolist()