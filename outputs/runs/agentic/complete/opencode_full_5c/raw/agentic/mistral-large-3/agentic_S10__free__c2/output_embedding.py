from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


def embed_output(
    texts: List[str], model_name: str = "all-MiniLM-L6-v2"
) -> List[List[float]]:
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()
