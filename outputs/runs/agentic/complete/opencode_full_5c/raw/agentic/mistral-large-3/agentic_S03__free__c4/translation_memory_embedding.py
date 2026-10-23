from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np


def translation_memory_embedding(segments: List[str]) -> List[List[float]]:
    """Embed translated segments for translation-memory search using SentenceTransformers."""
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = model.encode(segments, convert_to_numpy=True)
    return embeddings.tolist()
