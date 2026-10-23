from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

def translation_memory_embedding(texts: List[str]) -> List[List[float]]:
    """Embed translated segments for translation-memory search using SentenceTransformers."""
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = model.encode(texts, convert_to_tensor=False)
    return embeddings.tolist()