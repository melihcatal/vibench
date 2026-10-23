from typing import List
import os
from sentence_transformers import SentenceTransformer

def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(log_messages, convert_to_tensor=False)
    return embeddings.tolist()