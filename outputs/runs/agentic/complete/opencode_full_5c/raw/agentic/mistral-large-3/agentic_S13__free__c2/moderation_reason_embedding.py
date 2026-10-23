from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(rationales, convert_to_numpy=True)
    return embeddings.tolist()
